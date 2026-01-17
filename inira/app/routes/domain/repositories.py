from abc import ABC, abstractmethod
from typing import List, Optional
from inira.app.routes.domain.entities import RouteEntity


class RoutesRepository(ABC):

    @abstractmethod
    def save(self, route: RouteEntity) -> RouteEntity:
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> RouteEntity:
        pass

    @abstractmethod
    def all(self) -> List[RouteEntity]:
        pass

    @abstractmethod
    def paginate(
        self,
        *,
        page: int,
        page_size: int,
        difficulty: str | None = None,
        category: str | None = None,
    ) -> tuple[int, List[RouteEntity]]:
        """Retorna (total_count, routes)"""
        pass
