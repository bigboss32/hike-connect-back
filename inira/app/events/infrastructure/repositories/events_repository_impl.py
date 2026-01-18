# inira/app/events/infrastructure/repositories/events_repository_impl.py

from django.db.models import Count
from rest_framework.exceptions import NotFound

from inira.app.events.domain.entities import EventEntity
from inira.app.events.infrastructure.models import Evento


class EventsRepositoryImpl:

    def find_by_id(self, id: str) -> EventEntity:
        try:
            event = (
                Evento.objects
                .annotate(participants_count=Count("inscripciones"))
                .select_related("organized_by")
                .get(pk=id)
            )
        except Evento.DoesNotExist:
            raise NotFound("Evento no encontrado")

        return self._to_entity(event)

    def paginate(self, *, page: int, page_size: int):
        queryset = (
            Evento.objects
            .annotate(participants_count=Count("inscripciones"))
            .select_related("organized_by")
            .order_by("-date")
        )

        total = queryset.count()

        offset = (page - 1) * page_size
        queryset = queryset[offset: offset + page_size]

        events = [self._to_entity(e) for e in queryset]

        return total, events

    def _to_entity(self, model: Evento) -> EventEntity:
        return EventEntity(
            id=str(model.id),
            title=model.title,
            date=model.date,
            location=model.location,
            max_participants=model.max_participants,

            participants_count=model.participants_count,
            organized_by=(
                model.organized_by.username
                if model.organized_by else None
            ),

            meeting_point_lat=(
                model.meeting_point.y if model.meeting_point else None
            ),
            meeting_point_lng=(
                model.meeting_point.x if model.meeting_point else None
            ),
        )
