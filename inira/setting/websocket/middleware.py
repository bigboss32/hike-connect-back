# inira/setting/websocket/middleware.py

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()


@database_sync_to_async
def get_user_from_jwt(token_string):
    """
    Obtener usuario desde JWT token
    """
    try:
        # Validar y decodificar el token JWT
        access_token = AccessToken(token_string)
        user_id = access_token["user_id"]

        # Obtener el usuario
        user = User.objects.get(id=user_id)
        return user
    except (InvalidToken, TokenError, User.DoesNotExist, KeyError) as e:
        print(f"❌ Error validando JWT: {e}")
        return AnonymousUser()


class JWTAuthMiddleware:
    """
    Middleware para autenticar WebSockets con JWT de Simple JWT
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Obtener token de query string
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        if token:
            # Autenticar usuario con el token JWT
            scope["user"] = await get_user_from_jwt(token)
            print(f"🔑 JWT recibido, usuario: {scope['user']}")
        else:
            scope["user"] = AnonymousUser()
            print("⚠️ No se recibió token JWT")

        return await self.app(scope, receive, send)
