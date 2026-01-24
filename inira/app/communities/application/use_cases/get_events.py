# inira/app/events/domain/use_cases/get_events.py

from typing import Optional
from inira.app.events.domain.repositories.events_repository import EventsRepository


class GetEvents:
    def __init__(self, events_repository: EventsRepository):
        self.events_repository = events_repository

    def execute(
        self,
        *,
        id: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ):
        # 🔹 UN EVENTO
        if id:
            return self.events_repository.find_by_id(id)

        # 🔹 MUCHOS EVENTOS (PAGINADOS)
        total, events = self.events_repository.paginate(
            page=page,
            page_size=page_size,
        )

        return {
            "count": total,
            "page": page,
            "page_size": page_size,
            "results": events,
        }
