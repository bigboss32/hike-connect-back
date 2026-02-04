# inira/app/communities/infrastructure/repositories/member_repository_impl.py

from typing import List
from rest_framework.exceptions import NotFound

from inira.app.communities.domain.entities import MemberEntity
from inira.app.communities.domain.repositories.member_repository import MemberRepository
from inira.app.communities.infrastructure.models import ComunidadMember


class MemberRepositoryImpl(MemberRepository):

    def add_member(
        self, *, comunidad_id: str, user_id: int, role: str = "member"
    ) -> None:
        """Agregar un miembro a la comunidad"""
        ComunidadMember.objects.create(
            comunidad_id=comunidad_id, user_id=user_id, role=role
        )

    def remove_member(self, *, comunidad_id: str, user_id: int) -> None:
        """Remover un miembro de la comunidad"""
        member = ComunidadMember.objects.filter(
            comunidad_id=comunidad_id, user_id=user_id
        ).first()

        if not member:
            raise NotFound("No eres miembro de esta comunidad")

        member.delete()

    def exists(self, *, comunidad_id: str, user_id: int) -> bool:
        """Verificar si el usuario es miembro de la comunidad"""
        return ComunidadMember.objects.filter(
            comunidad_id=comunidad_id, user_id=user_id
        ).exists()

    def is_admin_or_owner(self, *, comunidad_id: str, user_id: int) -> bool:
        """Verificar si el usuario es admin u owner de la comunidad"""
        return ComunidadMember.objects.filter(
            comunidad_id=comunidad_id, user_id=user_id, role__in=["admin", "owner"]
        ).exists()

    def count_by_comunidad(self, comunidad_id: str) -> int:
        """Contar miembros de una comunidad"""
        return ComunidadMember.objects.filter(comunidad_id=comunidad_id).count()

    def find_by_comunidad(self, *, comunidad_id: str) -> List[MemberEntity]:
        """Obtener todos los miembros de una comunidad"""
        members = (
            ComunidadMember.objects.filter(comunidad_id=comunidad_id)
            .select_related("user")
            .order_by("-joined_at")
        )

        return [self._to_entity(member) for member in members]

    def count_by_user(self, *, user_id: int) -> int:
        """Contar el total de comunidades donde el usuario es miembro"""
        return ComunidadMember.objects.filter(user_id=user_id).count()

    def _to_entity(self, member: ComunidadMember) -> MemberEntity:
        """Convertir modelo Django a entidad de dominio"""
        return MemberEntity(
            id=str(member.id),
            comunidad_id=str(member.comunidad_id),
            user_id=member.user_id,
            user_name=(
                f"{member.user.first_name} {member.user.last_name}"
                if member.user
                else "Usuario"
            ),
            user_image=getattr(member.user, "profile_image", None),
            role=member.role,
            joined_at=member.joined_at,
        )
