# inira/app/communities/infrastructure/docs/post_community_member_docs.py

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes


post_community_member_docs = extend_schema(
       tags=["Comunidades - Miembros"],
    summary="Unirse a una comunidad",
    description="Permite al usuario autenticado unirse a una comunidad existente.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "comunidad_id": {"type": "string", "format": "uuid", "example": "a12f8400-e29b-41d4-a716-446655440111"},
            },
            "required": ["comunidad_id"],
        }
    },
    responses={
        201: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            name="Unión exitosa",
            value={"detail": "Te has unido a la comunidad exitosamente"},
            response_only=True,
            status_codes=["201"],
        ),
        OpenApiExample(
            name="comunidad_id requerido",
            value={"detail": "comunidad_id es requerido"},
            response_only=True,
            status_codes=["400"],
        ),
        OpenApiExample(
            name="Ya eres miembro",
            value={"detail": "Ya eres miembro de esta comunidad"},
            response_only=True,
            status_codes=["400"],
        ),
    ],
)