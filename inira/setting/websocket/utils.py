import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def broadcast_new_post(canal_id: str, post_data: dict):
    """
    Envía un nuevo post en tiempo real a todos los usuarios conectados al canal
    """
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"canal_chat_{canal_id}", {"type": "new_post", "post": post_data}
    )
