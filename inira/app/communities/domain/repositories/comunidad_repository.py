# inira/app/communities/domain/repositories/comunidad_repository.py

from abc import ABC, abstractmethod
from typing import Dict, List

from inira.app.communities.domain.entities import ComunidadEntity


class ComunidadRepository(ABC):

    @abstractmethod
    def find_by_id(self, comunidad_id: str, user_id: int = None) -> ComunidadEntity:
        pass

    @abstractmethod
    def find_all(self, *, page: int, page_size: int, user_id: int = None, **filters) -> Dict[str, any]:
        """Retorna {'results': List[ComunidadEntity], 'count': int}"""
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def exists(self, comunidad_id: str) -> bool:
        pass