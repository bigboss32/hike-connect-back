# inira/app/communities/infrastructure/docs/delete_community_member_docs.py

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes


delete_community_member_docs = extend_schema(
    tags=["Comunidades"],
    summary="Abandonar una comunidad",
    description="Permite al usuario autenticado salir de una comunidad.",
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
        204: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            name="Salida exitosa",
            value={"detail": "Has abandonado la comunidad"},
            response_only=True,
            status_codes=["204"],
        ),
        OpenApiExample(
            name="comunidad_id requerido",
            value={"detail": "comunidad_id es requerido"},
            response_only=True,
            status_codes=["400"],
        ),
        OpenApiExample(
            name="No eres miembro",
            value={"detail": "No eres miembro de esta comunidad"},
            response_only=True,
            status_codes=["400"],
        ),
    ],
)