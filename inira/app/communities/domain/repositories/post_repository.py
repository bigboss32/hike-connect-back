# inira/app/communities/domain/repositories/post_repository.py

from abc import ABC, abstractmethod
from typing import Dict

from inira.app.communities.domain.entities import PostEntity


class PostRepository(ABC):

    @abstractmethod
    def find_by_canal(self, *, canal_id: str, page: int, page_size: int) -> Dict[str, any]:
        """Retorna {'results': List[PostEntity], 'count': int}"""
        pass

    @abstractmethod
    def create(
        self,
        *,
        comunidad_id: str,
        canal_id: str,
        author_id: int,
        content: str,
    ) -> PostEntity:
        pass