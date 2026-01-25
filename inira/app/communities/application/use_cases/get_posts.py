# inira/app/communities/domain/use_cases/get_posts.py

from rest_framework.exceptions import ValidationError

from inira.app.communities.domain.repositories.post_repository import PostRepository
from inira.app.communities.domain.repositories.member_repository import MemberRepository
from inira.app.communities.domain.repositories.canal_repository import CanalRepository


class GetPosts:

    def __init__(
        self,
        post_repository: PostRepository,
        canal_repository: CanalRepository,
        member_repository: MemberRepository
    ):
        self.post_repository = post_repository
        self.canal_repository = canal_repository
        self.member_repository = member_repository

    def execute(self, *, canal_id: str, user_id: int, page: int = 1, page_size: int = 20):
        canal = self.canal_repository.find_by_id(canal_id)

        # Verificar que es miembro de la comunidad
        if not self.member_repository.exists(comunidad_id=canal.comunidad_id, user_id=user_id):
            raise ValidationError("Debes ser miembro de la comunidad para ver los posts")

        return self.post_repository.find_by_canal(
            canal_id=canal_id,
            page=page,
            page_size=page_size
        )