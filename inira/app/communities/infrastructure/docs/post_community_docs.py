# inira/app/communities/infrastructure/docs/post_community_docs.py

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes


post_community_docs = extend_schema(
     tags=["Comunidades - Gestión"],
    summary="Crear una nueva comunidad",
    description=(
        "Crea una nueva comunidad en el sistema.\n\n"
        "El usuario autenticado se convierte automáticamente en el creador y owner de la comunidad."
    ),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "example": "Aventureros de Bogotá"},
                "description": {"type": "string", "example": "Comunidad para amantes de la aventura"},
                "image": {"type": "string", "example": "https://example.com/image.jpg"},
                "company": {"type": "string", "example": "Adventure Co.", "nullable": True},
                "location": {"type": "string", "example": "Bogotá"},
                "is_public": {"type": "boolean", "example": True, "default": True},
            },
            "required": ["name", "description", "image", "location"],
        }
    },
    responses={
        201: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            name="Comunidad creada exitosamente",
            value={
                "id": "a12f8400-e29b-41d4-a716-446655440111",
                "name": "Aventureros de Bogotá",
                "description": "Comunidad para amantes de la aventura",
                "image": "https://example.com/image.jpg",
                "company": "Adventure Co.",
                "location": "Bogotá",
                "is_public": True,
                "created_at": "2025-01-24T10:00:00Z",
                "member_count": 1,
                "user_is_member": True,
                "canales": [],
                "created_by_name": "Juan Pérez",
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