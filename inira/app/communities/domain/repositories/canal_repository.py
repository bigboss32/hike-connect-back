# inira/app/communities/domain/repositories/canal_repository.py

from abc import ABC, abstractmethod
from typing import List

from inira.app.communities.domain.entities import CanalEntity


class CanalRepository(ABC):

    @abstractmethod
    def find_by_comunidad(self, comunidad_id: str) -> List[CanalEntity]:
        pass

    @abstractmethod
    def find_by_id(self, canal_id: str) -> CanalEntity:
        pass

    @abstractmethod
    def create(
        self,
        *,
        comunidad_id: str,
        name: str,
        description: str,
        is_info: bool,
        is_read_only: bool,
    ) -> CanalEntity:
        pass

    @abstractmethod
    def exists(self, canal_id: str) -> bool:
        pass