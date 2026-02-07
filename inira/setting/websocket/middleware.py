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
        print(f"✅ Usuario autenticado: {user.username} (ID: {user.id})")
        return user
    except (InvalidToken, TokenError) as e:
        print(f"❌ Token JWT inválido: {e}")
        return AnonymousUser()
    except User.DoesNotExist:
        print(f"❌ Usuario no existe con ID del token")
        return AnonymousUser()
    except KeyError as e:
        print(f"❌ Token no tiene campo user_id: {e}")
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
            print(f"🔑 Token recibido: {token[:50]}...")  # Solo primeros 50 chars
            scope["user"] = await get_user_from_jwt(token)
        else:
            print("⚠️ No se recibió token en query string")
            scope["user"] = AnonymousUser()

        return await self.app(scope, receive, send)
