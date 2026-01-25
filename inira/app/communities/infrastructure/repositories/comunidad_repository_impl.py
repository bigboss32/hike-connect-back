# inira/app/communities/infrastructure/repositories/comunidad_repository_impl.py

from django.db.models import Count, Q, Exists, OuterRef
from rest_framework.exceptions import NotFound

from inira.app.communities.domain.entities import ComunidadEntity
from inira.app.communities.domain.repositories.comunidad_repository import ComunidadRepository
from inira.app.communities.infrastructure.models import Comunidad, ComunidadMember


class ComunidadRepositoryImpl(ComunidadRepository):

    def find_by_id(self, comunidad_id: str, user_id: int = None) -> ComunidadEntity:
        try:
            queryset = Comunidad.objects.annotate(
                member_count=Count('members')
            ).select_related('created_by')
            
            # Agregar anotación para verificar si el usuario es miembro
            if user_id:
                queryset = queryset.annotate(
                    user_is_member=Exists(
                        ComunidadMember.objects.filter(
                            comunidad_id=OuterRef('id'),
                            user_id=user_id
                        )
                    )
                )
            
            comunidad = queryset.get(id=comunidad_id)
            
            return self._to_entity(comunidad, user_id=user_id)
        except Comunidad.DoesNotExist:
            raise NotFound("Comunidad no encontrada")

    def find_all(self, *, page: int, page_size: int, user_id: int = None, **filters):
        queryset = Comunidad.objects.annotate(
            member_count=Count('members')
        ).select_related('created_by')

        # Agregar anotación para verificar si el usuario es miembro
        if user_id:
            queryset = queryset.annotate(
                user_is_member=Exists(
                    ComunidadMember.objects.filter(
                        comunidad_id=OuterRef('id'),
                        user_id=user_id
                    )
                )
            )

        # Aplicar filtros
        if 'is_public' in filters:
            queryset = queryset.filter(is_public=filters['is_public'])

        # Paginación
        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        
        comunidades = queryset[start:end]
        
        return {
            'results': [self._to_entity(c, user_id=user_id) for c in comunidades],
            'count': total,
        }

    def create(
        self,
        *,
        name: str,
        description: str,
        image: str,
        created_by_id: int,
        company: str | None,
        location: str,
        is_public: bool,
    ) -> ComunidadEntity:
        comunidad = Comunidad.objects.create(
            name=name,
            description=description,
            image=image,
            created_by_id=created_by_id,
            company=company,
            location=location,
            is_public=is_public,
        )
        
        comunidad = Comunidad.objects.annotate(
            member_count=Count('members'),
            user_is_member=Exists(
                ComunidadMember.objects.filter(
                    comunidad_id=OuterRef('id'),
                    user_id=created_by_id
                )
            )
        ).select_related('created_by').get(id=comunidad.id)
        
        return self._to_entity(comunidad, user_id=created_by_id)

    def exists(self, comunidad_id: str) -> bool:
        return Comunidad.objects.filter(id=comunidad_id).exists()

    def _to_entity(self, comunidad: Comunidad, user_id: int = None) -> ComunidadEntity:
        return ComunidadEntity(
            id=str(comunidad.id),
            name=comunidad.name,
            description=comunidad.description,
            image=comunidad.image,
            company=comunidad.company,
            location=comunidad.location,
            is_public=comunidad.is_public,
            created_at=comunidad.created_at,
            created_by_id=comunidad.created_by_id,
            created_by_name=f"{comunidad.created_by.first_name} {comunidad.created_by.last_name}" if comunidad.created_by else None,
            member_count=getattr(comunidad, 'member_count', 0),
            user_is_member=getattr(comunidad, 'user_is_member', False),
        )