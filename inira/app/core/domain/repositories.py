from abc import ABC, abstractmethod

from app.Acta.domain.entities import ActaEntity


class ActaRepository(ABC):
    @abstractmethod
    def save(
        self, programa: ActaEntity
    ) -> ActaEntity:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> ActaEntity:
        pass

    @abstractmethod
    def find_by_llave(self, llave_id: str) -> ActaEntity:
        pass


