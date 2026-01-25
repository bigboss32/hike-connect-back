# inira/app/communities/infrastructure/repositories/member_repository_impl.py

from inira.app.communities.domain.repositories.member_repository import MemberRepository
from inira.app.communities.infrastructure.models import ComunidadMember


class MemberRepositoryImpl(MemberRepository):

    def add_member(self, *, comunidad_id: str, user_id: int, role: str = "member") -> None:
        ComunidadMember.objects.create(
            comunidad_id=comunidad_id,
            user_id=user_id,
            role=role,
        )

    def remove_member(self, *, comunidad_id: str, user_id: int) -> None:
        ComunidadMember.objects.filter(
            comunidad_id=comunidad_id,
            user_id=user_id
        ).delete()

    def exists(self, *, comunidad_id: str, user_id: int) -> bool:
        return ComunidadMember.objects.filter(
            comunidad_id=comunidad_id,
            user_id=user_id
        ).exists()

    def is_admin_or_owner(self, *, comunidad_id: str, user_id: int) -> bool:
        return ComunidadMember.objects.filter(
            comunidad_id=comunidad_id,
            user_id=user_id,
            role__in=["admin", "owner"]
        ).exists()

    def count_by_comunidad(self, comunidad_id: str) -> int:
        return ComunidadMember.objects.filter(comunidad_id=comunidad_id).count()