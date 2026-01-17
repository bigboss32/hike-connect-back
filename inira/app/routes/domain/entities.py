from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict


@dataclass
class Coordinates:
    lat: float
    lng: float


@dataclass
class RouteEntity:
    id: str
    title: str
    location: str
    distance: str
    duration: str
    difficulty: str
    image: str
    type: str
    category: str
    description: str
    coordinates: Coordinates

    company: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    whatsapp: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
