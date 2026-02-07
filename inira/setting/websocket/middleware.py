import logging
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()

logger = logging.getLogger("django")


@database_sync_to_async
def get_user_from_jwt(token_string):
    try:
        access_token = AccessToken(token_string)
        user_id = access_token.get("user_id")

        if not user_id:
            logger.warning("❌ JWT sin user_id")
            return AnonymousUser()

        user = User.objects.get(id=user_id)

        logger.info(f"✅ WS AUTH OK user_id={user.id} username={user.username}")

        return user

    except (InvalidToken, TokenError):
        logger.exception("❌ JWT inválido en WebSocket")
        return AnonymousUser()

    except User.DoesNotExist:
        logger.warning("❌ JWT válido pero usuario no existe")
        return AnonymousUser()

    except Exception:
        logger.exception("🔥 Error inesperado procesando JWT en WS")
        return AnonymousUser()


class JWTAuthMiddleware:
    """
    Middleware para autenticar WebSockets con JWT de Simple JWT
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()

        logger.info(f"🔍 WS query_string='{query_string[:200]}'")

        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        if token:
            logger.info(f"🔐 WS token recibido len={len(token)}")
            scope["user"] = await get_user_from_jwt(token)
        else:
            logger.warning("⚠️ WS conexión sin token JWT")
            scope["user"] = AnonymousUser()

        return await self.app(scope, receive, send)
