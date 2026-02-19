# inira/app/routes/domain/repositories.py

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
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
        difficulty: Optional[str] = None,
        category: Optional[str] = None,
        requires_payment: Optional[bool] = None,
        is_active: Optional[bool] = None,
    ) -> Tuple[int, List[RouteEntity]]:
        pass

    # 🆕 Métodos para gestión de disponibilidad
    @abstractmethod
    def get_availability_for_date(self, ruta_id: str, date):
        """Obtiene o crea la disponibilidad para una fecha específica"""
        pass

    @abstractmethod
    def check_availability(self, ruta_id: str, date, number_of_people: int) -> bool:
        """Verifica si hay cupos disponibles"""
        pass

    # inira/app/routes/domain/repositories.py — agregar abstractmethod

    @abstractmethod
    def paginate_by_user(
        self,
        *,
        user_id: str,
        page: int,
        page_size: int,
    ) -> Tuple[int, List[RouteEntity]]:
        pass
