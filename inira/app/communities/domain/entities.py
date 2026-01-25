# inira/app/communities/domain/entities.py

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ComunidadEntity:
    id: str
    name: str
    description: str
    image: str
    company: str | None
    location: str
    is_public: bool
    created_at: datetime
    created_by_id: int
    created_by_name: str | None
    member_count: int
    user_is_member: bool = False  # ← Agregar esto

@dataclass
class CanalEntity:
    id: str
    comunidad_id: str
    name: str
    description: str
    is_info: bool
    is_read_only: bool
    created_at: datetime
    post_count: int


@dataclass
class PostEntity:
    id: str
    comunidad_id: str
    canal_id: str
    author_id: int
    author_name: str
    author_image: str | None
    content: str
    created_at: datetime


@dataclass
class MemberEntity:
    id: str
    comunidad_id: str
    user_id: int
    role: str
    joined_at: datetime