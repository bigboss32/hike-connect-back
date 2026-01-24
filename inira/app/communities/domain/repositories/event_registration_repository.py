# inira/app/events/domain/repositories/event_registration_repository.py

from abc import ABC, abstractmethod


class EventRegistrationRepository(ABC):

    @abstractmethod
    def register(self, *, event_id: str, user_id: int) -> None:
        pass

    @abstractmethod
    def count_by_event(self, event_id: str) -> int:
        pass

    @abstractmethod
    def exists(self, *, event_id: str, user_id: int) -> bool:
        pass
