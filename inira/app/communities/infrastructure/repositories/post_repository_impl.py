# inira/app/communities/infrastructure/repositories/post_repository_impl.py

from django.db.models import F
from rest_framework.exceptions import NotFound

from inira.app.communities.domain.entities import PostEntity
from inira.app.communities.domain.repositories.post_repository import PostRepository
from inira.app.communities.infrastructure.models import ComunidadPost



class PostRepositoryImpl(PostRepository):

    def find_by_canal(self, *, canal_id: str, page: int, page_size: int):
        queryset = ComunidadPost.objects.filter(
            canal_id=canal_id
        ).select_related('author').order_by('created_at')

        # Paginación
        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        
        posts = queryset[start:end]
        
        return {
            'results': [self._to_entity(post) for post in posts],
            'count': total,
        }

    def create(
        self,
        *,
        comunidad_id: str,
        canal_id: str,
        author_id: int,
        content: str,
    ) -> PostEntity:
        post = ComunidadPost.objects.create(
            comunidad_id=comunidad_id,
            canal_id=canal_id,
            author_id=author_id,
            content=content,
        )
        
        post = ComunidadPost.objects.select_related('author').get(id=post.id)
        
        return self._to_entity(post)

    def _to_entity(self, post: ComunidadPost) -> PostEntity:
        return PostEntity(
            id=str(post.id),
            comunidad_id=str(post.comunidad_id),
            canal_id=str(post.canal_id),
            author_id=post.author_id,
            author_name=f"{post.author.first_name} {post.author.last_name}" if post.author else "Usuario",
            author_image=getattr(post.author, 'profile_image', None),
            content=post.content,
            created_at=post.created_at,
        )