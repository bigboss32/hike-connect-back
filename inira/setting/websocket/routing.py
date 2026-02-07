# routing.py

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Agrega el ^ al inicio del regex
    re_path(
        r"^ws/chat/canal/(?P<canal_id>[0-9a-f-]+)/$",  # ← Agrega ^
        consumers.CanalChatConsumer.as_asgi(),
    ),
]
