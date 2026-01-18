# inira/app/events/infrastructure/repositories/event_registration_repository_impl.py

from inira.app.events.domain.repositories.event_registration_repository import (
    EventRegistrationRepository
)
from inira.app.events.infrastructure.models import EventoInscripcion


class EventRegistrationRepositoryImpl(EventRegistrationRepository):

    def register(self, *, event_id: str, user_id: int) -> None:
        EventoInscripcion.objects.create(
            evento_id=event_id,
            user_id=user_id,
        )

    def count_by_event(self, event_id: str) -> int:
        return EventoInscripcion.objects.filter(evento_id=event_id).count()

    def exists(self, *, event_id: str, user_id: int) -> bool:
        return EventoInscripcion.objects.filter(
            evento_id=event_id,
            user_id=user_id,
        ).exists()
