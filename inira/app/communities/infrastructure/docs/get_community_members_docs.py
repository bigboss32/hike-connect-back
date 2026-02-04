# inira/app/communities/infrastructure/docs/get_community_members_docs.py

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
)
from drf_spectacular.types import OpenApiTypes


get_community_members_docs = extend_schema(
    tags=["Comunidades - Miembros"],
    summary="Obtener miembros de comunidad o estadísticas del usuario",
    description=(
        "Este endpoint tiene dos modos de operación:\n\n"
        "**Modo 1: Obtener miembros de una comunidad**\n"
        "- Query param: `comunidad_id` (UUID)\n"
        "- Retorna: Lista de miembros de la comunidad\n"
        "- Nota: Si la comunidad es privada, solo los miembros pueden ver la lista\n\n"
        "**Modo 2: Obtener estadísticas del usuario**\n"
        "- Query param: `stats=true`\n"
        "- Retorna: Total de comunidades donde el usuario es miembro"
    ),
    parameters=[
        OpenApiParameter(
            name="comunidad_id",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            description="ID de la comunidad (requerido para Modo 1)",
            required=False,
            examples=[
                OpenApiExample(
                    name="UUID ejemplo",
                    value="a12f8400-e29b-41d4-a716-446655440111",
                ),
            ],
        ),
        OpenApiParameter(
            name="stats",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Debe ser 'true' para obtener estadísticas (Modo 2)",
            required=False,
            examples=[
                OpenApiExample(
                    name="Obtener estadísticas",
                    value="true",
                ),
            ],
        ),
    ],
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
        403: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            name="Lista de miembros exitosa (Modo 1)",
            value={
                "count": 3,
                "results": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "comunidad_id": "a12f8400-e29b-41d4-a716-446655440111",
                        "user_id": 42,
                        "user_name": "Juan Pérez",
                        "user_image": "https://example.com/images/juan.jpg",
                        "role": "owner",
                        "joined_at": "2024-01-15T10:30:00Z",
                    },
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174001",
                        "comunidad_id": "a12f8400-e29b-41d4-a716-446655440111",
                        "user_id": 43,
                        "user_name": "María García",
                        "user_image": None,
                        "role": "member",
                        "joined_at": "2024-01-16T14:20:00Z",
                    },
                ],
            },
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            name="Estadísticas del usuario exitosas (Modo 2)",
            value={"total_communities": 7},
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            name="Parámetros requeridos",
            value={"detail": "Se requiere 'comunidad_id' o 'stats=true'"},
            response_only=True,
            status_codes=["400"],
        ),
        OpenApiExample(
            name="Sin permisos - Comunidad privada",
            value={
                "detail": "No tienes permisos para ver los miembros de esta comunidad privada"
            },
            response_only=True,
            status_codes=["403"],
        ),
        OpenApiExample(
            name="Comunidad no encontrada",
            value={"detail": "Comunidad no encontrada"},
            response_only=True,
            status_codes=["404"],
        ),
    ],
)
