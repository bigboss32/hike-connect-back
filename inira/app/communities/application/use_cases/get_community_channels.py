# inira/app/communities/domain/use_cases/get_community_channels.py

from rest_framework.exceptions import ValidationError

from inira.app.communities.domain.repositories.canal_repository import CanalRepository
from inira.app.communities.domain.repositories.member_repository import MemberRepository


class GetCommunityChannels:

    def __init__(
        self,
        canal_repository: CanalRepository,
        member_repository: MemberRepository
    ):
        self.canal_repository = canal_repository
        self.member_repository = member_repository

    def execute(self, *, comunidad_id: str, user_id: int):
        # Verificar que es miembro
        if not self.member_repository.exists(comunidad_id=comunidad_id, user_id=user_id):
            raise ValidationError("Debes ser miembro de la comunidad para ver sus canales")

        return self.canal_repository.find_by_comunidad(comunidad_id)