# inira/app/communities/infrastructure/docs/get_community_channels_docs.py

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes


get_community_channels_docs = extend_schema(
     tags=["Comunidades - Canales"],
    summary="Obtener canales de una comunidad",
    description="Obtiene todos los canales de una comunidad específica.",
    parameters=[
        OpenApiParameter(
            name="comunidad_id",
            description="ID UUID de la comunidad",
            required=True,
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
        ),
    ],
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            name="Lista de canales",
            value=[
                {
                    "id": "c44e8400-e29b-41d4-a716-446655440333",
                    "name": "general",
                    "description": "Canal general de la comunidad",
                    "is_info": False,
                    "is_read_only": False,
                    "created_at": "2025-01-15T10:05:00Z",
                    "post_count": 15,
                },
                {
                    "id": "d55e8400-e29b-41d4-a716-446655440444",
                    "name": "anuncios",
                    "description": "Canal de anuncios importantes",
                    "is_info": True,
                    "is_read_only": True,
                    "created_at": "2025-01-15T10:06:00Z",
                    "post_count": 3,
                }
            ],
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            name="comunidad_id requerido",
            value={"detail": "comunidad_id es requerido"},
            response_only=True,
            status_codes=["400"],
        ),
    ],
)