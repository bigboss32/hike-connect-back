# inira/app/communities/domain/use_cases/create_post.py

from rest_framework.exceptions import ValidationError

from inira.app.communities.domain.repositories.post_repository import PostRepository
from inira.app.communities.domain.repositories.member_repository import MemberRepository
from inira.app.communities.domain.repositories.canal_repository import CanalRepository


class CreatePost:

    def __init__(
        self,
        post_repository: PostRepository,
        canal_repository: CanalRepository,
        member_repository: MemberRepository
    ):
        self.post_repository = post_repository
        self.canal_repository = canal_repository
        self.member_repository = member_repository

    def execute(
        self,
        *,
        comunidad_id: str,
        canal_id: str,
        author_id: int,
        content: str,
    ):
        # Verificar que es miembro
        if not self.member_repository.exists(comunidad_id=comunidad_id, user_id=author_id):
            raise ValidationError("Debes ser miembro de la comunidad para publicar")

        canal = self.canal_repository.find_by_id(canal_id)

        # Verificar si el canal es read-only
        if canal.is_read_only:
            if not self.member_repository.is_admin_or_owner(comunidad_id=comunidad_id, user_id=author_id):
                raise ValidationError("Solo los administradores pueden publicar en este canal")

        if not content:
            raise ValidationError("El contenido no puede estar vacío")

        return self.post_repository.create(
            comunidad_id=comunidad_id,
            canal_id=canal_id,
            author_id=author_id,
            content=content,
        )