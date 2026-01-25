# inira/app/communities/domain/use_cases/join_community.py

from rest_framework.exceptions import ValidationError

from inira.app.communities.domain.repositories.comunidad_repository import ComunidadRepository
from inira.app.communities.domain.repositories.member_repository import MemberRepository


class JoinCommunity:

    def __init__(
        self,
        comunidad_repository: ComunidadRepository,
        member_repository: MemberRepository
    ):
        self.comunidad_repository = comunidad_repository
        self.member_repository = member_repository

    def execute(self, *, comunidad_id: str, user_id: int):
        # Verificar que la comunidad existe
        comunidad = self.comunidad_repository.find_by_id(comunidad_id)

        # Verificar que no es miembro
        if self.member_repository.exists(comunidad_id=comunidad_id, user_id=user_id):
            raise ValidationError("Ya eres miembro de esta comunidad")

        # Agregar como miembro
        self.member_repository.add_member(
            comunidad_id=comunidad_id,
            user_id=user_id,
            role="member"
        )