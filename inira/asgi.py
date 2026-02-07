# inira/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inira.settings")

django_asgi_app = get_asgi_application()

# ✅ Importar DESPUÉS de get_asgi_application()
from inira.setting.websocket import routing
from inira.setting.websocket.middleware import JWTAuthMiddleware

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": JWTAuthMiddleware(URLRouter(routing.websocket_urlpatterns)),
    }
)
