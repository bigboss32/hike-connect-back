# inira/app/communities/infrastructure/docs/post_community_channel_docs.py

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes


post_community_channel_docs = extend_schema(
    tags=["Comunidades - Canales"],
    summary="Crear un canal en una comunidad",
    description=(
        "Crea un nuevo canal dentro de una comunidad.\n\n"
        "Solo los administradores y owners de la comunidad pueden crear canales."
    ),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "comunidad_id": {"type": "string", "format": "uuid", "example": "a12f8400-e29b-41d4-a716-446655440111"},
                "name": {"type": "string", "example": "eventos"},
                "description": {"type": "string", "example": "Canal para organizar eventos"},
                "is_info": {"type": "boolean", "example": False, "default": False},
                "is_read_only": {"type": "boolean", "example": False, "default": False},
            },
            "required": ["comunidad_id", "name"],
        }
    },
    responses={
        201: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            name="Canal creado exitosamente",
            value={
                "id": "c44e8400-e29b-41d4-a716-446655440333",
                "name": "eventos",
                "description": "Canal para organizar eventos",
                "is_info": False,
                "is_read_only": False,
                "created_at": "2025-01-24T10:00:00Z",
                "post_count": 0,
            },
            response_only=True,
            status_codes=["201"],
        ),
        OpenApiExample(
            name="Error de validación",
            value={"detail": "name es requerido"},
            response_only=True,
            status_codes=["400"],
        ),
    ],
)