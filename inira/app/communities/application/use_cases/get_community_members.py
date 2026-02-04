# inira/app/communities/domain/use_cases/get_community_members.py

from typing import List
from rest_framework.exceptions import PermissionDenied

from inira.app.communities.domain.entities import MemberEntity
from inira.app.communities.domain.repositories.comunidad_repository import (
    ComunidadRepository,
)
from inira.app.communities.domain.repositories.member_repository import MemberRepository


class GetCommunityMembers:

    def __init__(
        self,
        comunidad_repository: ComunidadRepository,
        member_repository: MemberRepository,
    ):
        self.comunidad_repository = comunidad_repository
        self.member_repository = member_repository

    def execute(self, *, comunidad_id: str, user_id: int) -> List[MemberEntity]:
        # Verificar que la comunidad existe
        comunidad = self.comunidad_repository.find_by_id(comunidad_id)

        # Si la comunidad es privada, verificar que el usuario es miembro
        if not comunidad.is_public:
            if not self.member_repository.exists(
                comunidad_id=comunidad_id, user_id=user_id
            ):
                raise PermissionDenied(
                    "No tienes permisos para ver los miembros de esta comunidad privada"
                )

        # Obtener los miembros
        members = self.member_repository.find_by_comunidad(comunidad_id=comunidad_id)

        return members
