# inira/app/communities/domain/use_cases/leave_community.py

from rest_framework.exceptions import ValidationError

from inira.app.communities.domain.repositories.member_repository import MemberRepository


class LeaveCommunity:

    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository

    def execute(self, *, comunidad_id: str, user_id: int):
        # Verificar que es miembro
        if not self.member_repository.exists(comunidad_id=comunidad_id, user_id=user_id):
            raise ValidationError("No eres miembro de esta comunidad")

        # Remover miembro
        self.member_repository.remove_member(
            comunidad_id=comunidad_id,
            user_id=user_id
        )