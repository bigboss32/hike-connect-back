# inira/app/communities/infrastructure/docs/post_community_post_docs.py

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes


post_community_post_docs = extend_schema(
     tags=["Comunidades - Posts"],
    summary="Crear un post en un canal",
    description="Crea un nuevo post dentro de un canal de una comunidad.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "comunidad_id": {"type": "string", "format": "uuid", "example": "a12f8400-e29b-41d4-a716-446655440111"},
                "canal_id": {"type": "string", "format": "uuid", "example": "c44e8400-e29b-41d4-a716-446655440333"},
                "content": {"type": "string", "example": "¡Hola a todos! Este es mi primer post."},
            },
            "required": ["comunidad_id", "canal_id", "content"],
        }
    },
    responses={
        201: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            name="Post creado exitosamente",
            value={
                "id": "e66e8400-e29b-41d4-a716-446655440555",
                "content": "¡Hola a todos! Este es mi primer post.",
                "created_at": "2025-01-24T10:00:00Z",
                "author_name": "Juan Pérez",
                "author_image": "https://example.com/profile.jpg",
            },
            response_only=True,
            status_codes=["201"],
        ),
        OpenApiExample(
            name="Error de validación",
            value={"detail": "content es requerido"},
            response_only=True,
            status_codes=["400"],
        ),
    ],
)