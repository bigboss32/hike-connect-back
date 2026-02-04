# inira/app/communities/domain/repositories/member_repository.py

from abc import ABC, abstractmethod
from typing import List


class MemberRepository(ABC):

    @abstractmethod
    def add_member(
        self, *, comunidad_id: str, user_id: int, role: str = "member"
    ) -> None:
        pass

    @abstractmethod
    def remove_member(self, *, comunidad_id: str, user_id: int) -> None:
        pass

    @abstractmethod
    def exists(self, *, comunidad_id: str, user_id: int) -> bool:
        pass

    @abstractmethod
    def is_admin_or_owner(self, *, comunidad_id: str, user_id: int) -> bool:
        pass

    @abstractmethod
    def count_by_comunidad(self, comunidad_id: str) -> int:
        pass

    @abstractmethod
    def find_by_comunidad(self, *, comunidad_id: str) -> List:
        """Obtener todos los miembros de una comunidad"""
        pass

    @abstractmethod
    def count_by_user(self, *, user_id: int) -> int:
        """Contar el total de comunidades donde el usuario es miembro"""
        pass
