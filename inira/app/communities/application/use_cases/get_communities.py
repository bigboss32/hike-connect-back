# inira/app/communities/application/use_cases/get_communities.py

from inira.app.communities.domain.repositories.comunidad_repository import ComunidadRepository


class GetCommunities:

    def __init__(self, comunidad_repository: ComunidadRepository):
        self.comunidad_repository = comunidad_repository

    def execute(self, *, id: str = None, user_id: int, page: int = 1, page_size: int = 10, **filters):
        if id:
            return self.comunidad_repository.find_by_id(id, user_id=user_id)  # ✅ Agregar user_id
        
        return self.comunidad_repository.find_all(
            page=page,
            page_size=page_size,
            user_id=user_id,  # ✅ Agregar user_id
            **filters
        )