# inira/app/events/domain/entities.py


from dataclasses import dataclass
from datetime import datetime


@dataclass
class EventEntity:
    id: str
    title: str
    date: datetime
    location: str
    max_participants: int

    participants_count: int
    organized_by: str | None

    meeting_point_lat: float | None
    meeting_point_lng: float | None
