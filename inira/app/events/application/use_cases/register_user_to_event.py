# inira/app/events/domain/use_cases/register_user_to_event.py

from rest_framework.exceptions import ValidationError

from inira.app.events.domain.repositories.event_registration_repository import EventRegistrationRepository
from inira.app.events.domain.repositories.events_repository import EventsRepository


class RegisterUserToEvent:

    def __init__(self, events_repository:EventsRepository, registration_repository:EventRegistrationRepository):
        self.events_repository = events_repository
        self.registration_repository = registration_repository

    def execute(self, *, event_id: str, user_id: int):

        event = self.events_repository.find_by_id(event_id)

        if self.registration_repository.exists(
            event_id=event_id,
            user_id=user_id,
        ):
            raise ValidationError("Ya estás inscrito en este evento")

        total = self.registration_repository.count_by_event(event_id)
        if total >= event.max_participants:
            raise ValidationError("Evento lleno")

        self.registration_repository.register(
            event_id=event_id,
            user_id=user_id,
        )
