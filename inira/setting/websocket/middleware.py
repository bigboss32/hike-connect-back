# inira/setting/websocket/middleware.py

import logging
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()

logger = logging.getLogger(__name__)


@database_sync_to_async
def get_user_from_jwt(token_string):
    """
    Obtener usuario desde JWT token
    """
    try:
        access_token = AccessToken(token_string)
        user_id = access_token["user_id"]

        user = User.objects.get(id=user_id)

        logger.info(
            "Usuario autenticado vía WebSocket",
            extra={"user_id": user.id, "username": user.username},
        )

        return user

    except (InvalidToken, TokenError) as e:
        logger.warning("Token JWT inválido en WebSocket", exc_info=e)
        return AnonymousUser()

    except User.DoesNotExist:
        logger.warning("Usuario no existe con ID del token JWT")
        return AnonymousUser()

    except KeyError as e:
        logger.error("Token JWT no contiene campo user_id", exc_info=e)
        return AnonymousUser()


class JWTAuthMiddleware:
    """
    Middleware para autenticar WebSockets con JWT de Simple JWT
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        if token:
            logger.info("Token recibido en WebSocket (parcial): %s...", token[:50])
            scope["user"] = await get_user_from_jwt(token)
        else:
            logger.info("Conexión WebSocket sin token JWT")
            scope["user"] = AnonymousUser()

        return await self.app(scope, receive, send)
