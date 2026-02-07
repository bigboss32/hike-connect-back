import json
import logging
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

logger = logging.getLogger("django")  # Render captura este


class CanalChatConsumer(AsyncWebsocketConsumer):
    """
    Consumer para posts en tiempo real de canales - CON SEGURIDAD
    """

    async def connect(self):
        self.canal_id = self.scope["url_route"]["kwargs"]["canal_id"]
        self.user = self.scope.get("user")

        logger.info(f"🔌 Intento conexión WS canal={self.canal_id}")

        # ✅ SEGURIDAD 1: Verificar autenticación
        if not self.user or not self.user.is_authenticated:
            logger.warning(
                f"❌ WS RECHAZADO - Usuario no autenticado canal={self.canal_id}"
            )
            await self.close(code=4001)
            return

        # ✅ SEGURIDAD 2: Verificar membresía del canal
        is_member = await self.check_canal_membership()
        if not is_member:
            logger.warning(
                f"❌ WS RECHAZADO - Usuario {self.user.username} no es miembro "
                f"canal={self.canal_id}"
            )
            await self.close(code=4003)
            return

        # ✅ SEGURIDAD 3: Verificar permisos de escritura
        self.can_write = await self.check_write_permission()

        self.room_group_name = f"canal_chat_{self.canal_id}"

        # Unirse al grupo
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        logger.info(
            f"✅ WS CONECTADO usuario={self.user.username} canal={self.canal_id}"
        )

        await self.send(
            text_data=json.dumps(
                {
                    "type": "connection_established",
                    "canal_id": self.canal_id,
                    "user_id": self.user.id,
                    "username": self.user.username,
                    "can_write": self.can_write,
                    "message": "Conectado al canal exitosamente",
                    "timestamp": self.get_timestamp(),
                }
            )
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_joined",
                "user_id": self.user.id,
                "username": self.user.username,
                "timestamp": self.get_timestamp(),
            },
        )

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name") and hasattr(self, "user"):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_left",
                    "user_id": self.user.id,
                    "username": self.user.username,
                    "timestamp": self.get_timestamp(),
                },
            )

            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

        logger.info(
            f"🔌 WS DESCONECTADO canal={self.canal_id} "
            f"user={getattr(self.user, 'username', None)} "
            f"code={close_code}"
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get("type", "message")

            if message_type == "ping":
                await self.send(
                    text_data=json.dumps(
                        {"type": "pong", "timestamp": self.get_timestamp()}
                    )
                )

            elif message_type == "typing":
                if not self.can_write:
                    logger.warning(
                        f"🚫 Usuario {self.user.username} intentó escribir sin permiso "
                        f"canal={self.canal_id}"
                    )
                    await self.send(
                        text_data=json.dumps(
                            {
                                "type": "error",
                                "message": "No tienes permiso para escribir en este canal",
                            }
                        )
                    )
                    return

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "user_typing",
                        "user_id": self.user.id,
                        "username": self.user.username,
                        "is_typing": data.get("is_typing", True),
                    },
                )

        except json.JSONDecodeError:
            logger.error("❌ JSON inválido recibido por WS", exc_info=True)
            await self.send(
                text_data=json.dumps({"type": "error", "message": "JSON inválido"})
            )

        except Exception:
            logger.exception("🔥 Error inesperado en WS receive()")
            await self.send(
                text_data=json.dumps(
                    {"type": "error", "message": "Error interno del servidor"}
                )
            )

    async def new_post(self, event):
        await self.send(
            text_data=json.dumps({"type": "new_post", "post": event["post"]})
        )

    async def user_joined(self, event):
        if event["user_id"] != self.user.id:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "user_joined",
                        "user_id": event["user_id"],
                        "username": event["username"],
                        "timestamp": event["timestamp"],
                    }
                )
            )

    async def user_left(self, event):
        if event["user_id"] != self.user.id:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "user_left",
                        "user_id": event["user_id"],
                        "username": event["username"],
                        "timestamp": event["timestamp"],
                    }
                )
            )

    async def user_typing(self, event):
        if event["user_id"] != self.user.id:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "typing",
                        "user_id": event["user_id"],
                        "username": event["username"],
                        "is_typing": event["is_typing"],
                    }
                )
            )

    @database_sync_to_async
    def check_canal_membership(self):
        from inira.app.shared.container import container

        try:
            canal_repo = container.communities().canal_repository()
            member_repo = container.communities().member_repository()

            canal = canal_repo.find_by_id(self.canal_id)

            return member_repo.exists(
                comunidad_id=str(canal.comunidad_id),
                user_id=self.user.id,
            )

        except Exception:
            logger.exception(f"🔥 Error verificando membresía canal={self.canal_id}")
            return False

    @database_sync_to_async
    def check_write_permission(self):
        from inira.app.shared.container import container

        try:
            canal_repo = container.communities().canal_repository()
            member_repo = container.communities().member_repository()

            canal = canal_repo.find_by_id(self.canal_id)

            if canal.is_read_only:
                return member_repo.is_admin_or_owner(
                    comunidad_id=str(canal.comunidad_id),
                    user_id=self.user.id,
                )

            return True

        except Exception:
            logger.exception(f"🔥 Error verificando permisos canal={self.canal_id}")
            return False

    def get_timestamp(self):
        return datetime.now().isoformat()
