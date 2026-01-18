# inira/app/events/domain/repositories/events_repository.py

from abc import ABC, abstractmethod
from inira.app.events.domain.entities import EventEntity
from typing import List, Tuple

class EventsRepository(ABC):

    @abstractmethod
    def find_by_id(self, id: str) -> EventEntity:
        pass


    @abstractmethod
    def paginate(
        self,
        *,
        page: int,
        page_size: int,
    ) -> Tuple[int, List[EventEntity]]:
        pass
