# inira/app/communities/infrastructure/repositories/canal_repository_impl.py

from django.db.models import Count
from rest_framework.exceptions import NotFound

from inira.app.communities.domain.entities import CanalEntity
from inira.app.communities.domain.repositories.canal_repository import CanalRepository
from inira.app.communities.infrastructure.models import ComunidadCanal


class CanalRepositoryImpl(CanalRepository):

    def find_by_comunidad(self, comunidad_id: str) -> list[CanalEntity]:
        canales = ComunidadCanal.objects.filter(
            comunidad_id=comunidad_id
        ).annotate(
            post_count=Count('posts')
        ).order_by('created_at')
        
        return [self._to_entity(canal) for canal in canales]

    def find_by_id(self, canal_id: str) -> CanalEntity:
        try:
            canal = ComunidadCanal.objects.annotate(
                post_count=Count('posts')
            ).get(id=canal_id)
            
            return self._to_entity(canal)
        except ComunidadCanal.DoesNotExist:
            raise NotFound("Canal no encontrado")

    def create(
        self,
        *,
        comunidad_id: str,
        name: str,
        description: str,
        is_info: bool,
        is_read_only: bool,
    ) -> CanalEntity:
        canal = ComunidadCanal.objects.create(
            comunidad_id=comunidad_id,
            name=name,
            description=description,
            is_info=is_info,
            is_read_only=is_read_only,
        )
        
        canal = ComunidadCanal.objects.annotate(
            post_count=Count('posts')
        ).get(id=canal.id)
        
        return self._to_entity(canal)

    def exists(self, canal_id: str) -> bool:
        return ComunidadCanal.objects.filter(id=canal_id).exists()

    def _to_entity(self, canal: ComunidadCanal) -> CanalEntity:
        return CanalEntity(
            id=str(canal.id),
            comunidad_id=str(canal.comunidad_id),
            name=canal.name,
            description=canal.description,
            is_info=canal.is_info,
            is_read_only=canal.is_read_only,
            created_at=canal.created_at,
            post_count=getattr(canal, 'post_count', 0),
        )