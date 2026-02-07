# consumers.py - CanalChatConsumer CON SEGURIDAD

import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class CanalChatConsumer(AsyncWebsocketConsumer):
    """
    Consumer para posts en tiempo real de canales - CON SEGURIDAD
    """

    async def connect(self):
        self.canal_id = self.scope["url_route"]["kwargs"]["canal_id"]
        self.user = self.scope.get("user")

        # ✅ SEGURIDAD 1: Verificar autenticación
        if not self.user or not self.user.is_authenticated:
            print(
                f"❌ Usuario no autenticado intentó conectar al canal {self.canal_id}"
            )
            await self.close(code=4001)  # 4001 = No autorizado
            return

        # ✅ SEGURIDAD 2: Verificar membresía del canal
        is_member = await self.check_canal_membership()
        if not is_member:
            print(
                f"❌ Usuario {self.user.username} no es miembro del canal {self.canal_id}"
            )
            await self.close(code=4003)  # 4003 = Forbidden
            return

        # ✅ SEGURIDAD 3: Verificar permisos de escritura
        self.can_write = await self.check_write_permission()

        self.room_group_name = f"canal_chat_{self.canal_id}"

        # Unirse al grupo
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Aceptar conexión
        await self.accept()

        # Enviar confirmación
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

        # Notificar a otros que este usuario se conectó
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_joined",
                "user_id": self.user.id,
                "username": self.user.username,
                "timestamp": self.get_timestamp(),
            },
        )

        print(f"✅ Usuario {self.user.username} conectado al canal {self.canal_id}")

    async def disconnect(self, close_code):
        # Notificar que usuario se desconectó
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

        print(f"❌ Usuario desconectado del canal {self.canal_id} - Code: {close_code}")

    async def receive(self, text_data):
        """Recibir mensaje del cliente"""
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
                # ✅ SEGURIDAD: Solo usuarios autenticados pueden enviar typing
                if not self.can_write:
                    await self.send(
                        text_data=json.dumps(
                            {
                                "type": "error",
                                "message": "No tienes permiso para escribir en este canal",
                            }
                        )
                    )
                    return

                # Broadcast indicador de escritura
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
            await self.send(
                text_data=json.dumps({"type": "error", "message": "JSON inválido"})
            )
        except Exception as e:
            await self.send(text_data=json.dumps({"type": "error", "message": str(e)}))

    async def new_post(self, event):
        """Enviar nuevo post al cliente en tiempo real"""
        await self.send(
            text_data=json.dumps({"type": "new_post", "post": event["post"]})
        )

    async def user_joined(self, event):
        """Notificar que un usuario se conectó"""
        # No enviar al mismo usuario
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
        """Notificar que un usuario se desconectó"""
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
        """Notificar que usuario está escribiendo"""
        # No enviar al mismo usuario
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
        """Verificar que el usuario es miembro del canal"""
        from inira.app.shared.container import container

        try:
            canal_repo = container.communities().canal_repository()
            member_repo = container.communities().member_repository()

            canal = canal_repo.find_by_id(self.canal_id)
            return member_repo.exists(
                comunidad_id=str(canal.comunidad_id), user_id=self.user.id
            )
        except Exception as e:
            print(f"❌ Error verificando membresía: {e}")
            return False

    @database_sync_to_async
    def check_write_permission(self):
        """Verificar si el usuario puede escribir en el canal"""
        from inira.app.shared.container import container

        try:
            canal_repo = container.communities().canal_repository()
            member_repo = container.communities().member_repository()

            canal = canal_repo.find_by_id(self.canal_id)

            # Si el canal es read-only, solo admins pueden escribir
            if canal.is_read_only:
                return member_repo.is_admin_or_owner(
                    comunidad_id=str(canal.comunidad_id), user_id=self.user.id
                )

            # Si no es read-only, todos los miembros pueden escribir
            return True
        except Exception as e:
            print(f"❌ Error verificando permisos: {e}")
            return False

    def get_timestamp(self):
        return datetime.now().isoformat()
