# inira/app/communities/domain/use_cases/create_community.py

from rest_framework.exceptions import ValidationError

from inira.app.communities.domain.repositories.comunidad_repository import ComunidadRepository
from inira.app.communities.domain.repositories.member_repository import MemberRepository


class CreateCommunity:

    def __init__(
        self,
        comunidad_repository: ComunidadRepository,
        member_repository: MemberRepository
    ):
        self.comunidad_repository = comunidad_repository
        self.member_repository = member_repository

    def execute(
        self,
        *,
        name: str,
        description: str,
        image: str,
        created_by_id: int,
        company: str | None = None,
        location: str,
        is_public: bool = True,
    ):
        if not name or not description or not image or not location:
            raise ValidationError("Todos los campos obligatorios deben ser proporcionados")

        comunidad = self.comunidad_repository.create(
            name=name,
            description=description,
            image=image,
            created_by_id=created_by_id,
            company=company,
            location=location,
            is_public=is_public,
        )

        # Agregar al creador como owner
        self.member_repository.add_member(
            comunidad_id=str(comunidad.id),
            user_id=created_by_id,
            role="owner"
        )

        return comunidad