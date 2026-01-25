# inira/app/communities/domain/use_cases/create_channel.py

from rest_framework.exceptions import ValidationError

from inira.app.communities.domain.repositories.canal_repository import CanalRepository
from inira.app.communities.domain.repositories.member_repository import MemberRepository


class CreateChannel:

    def __init__(
        self,
        canal_repository: CanalRepository,
        member_repository: MemberRepository
    ):
        self.canal_repository = canal_repository
        self.member_repository = member_repository

    def execute(
        self,
        *,
        comunidad_id: str,
        name: str,
        description: str = "",
        is_info: bool = False,
        is_read_only: bool = False,
        user_id: int,
    ):
        # Verificar que es admin u owner
        if not self.member_repository.is_admin_or_owner(comunidad_id=comunidad_id, user_id=user_id):
            raise ValidationError("Solo los administradores pueden crear canales")

        if not name:
            raise ValidationError("El nombre del canal es requerido")

        return self.canal_repository.create(
            comunidad_id=comunidad_id,
            name=name,
            description=description,
            is_info=is_info,
            is_read_only=is_read_only,
        )