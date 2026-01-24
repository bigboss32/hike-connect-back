# inira/app/communities/infrastructure/docs/get_community_posts_docs.py

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes


get_community_posts_docs = extend_schema(
     tags=["Comunidades - Posts"],
    summary="Obtener posts de un canal",
    description="Obtiene todos los posts de un canal específico con paginación.",
    parameters=[
        OpenApiParameter(
            name="canal_id",
            description="ID UUID del canal",
            required=True,
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="page",
            description="Número de página (default = 1)",
            required=False,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="page_size",
            description="Cantidad de resultados por página (default = 20)",
            required=False,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
        ),
    ],
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            name="Lista de posts",
            value={
                "count": 25,
                "page": 1,
                "page_size": 20,
                "results": [
                    {
                        "id": "e66e8400-e29b-41d4-a716-446655440555",
                        "content": "¡Bienvenidos al canal de eventos!",
                        "created_at": "2025-01-24T09:00:00Z",
                        "author_name": "Juan Pérez",
                        "author_image": "https://example.com/profile.jpg",
                    },
                    {
                        "id": "f77e8400-e29b-41d4-a716-446655440666",
                        "content": "Próximo evento este sábado",
                        "created_at": "2025-01-24T10:30:00Z",
                        "author_name": "María García",
                        "author_image": None,
                    }
                ]
            },
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            name="canal_id requerido",
            value={"detail": "canal_id es requerido"},
            response_only=True,
            status_codes=["400"],
        ),
    ],
)