# inira/app/communities/infrastructure/docs/get_communities_docs.py

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes


get_communities_docs = extend_schema(
     tags=["Comunidades - Gestión"],
    summary="Obtener comunidades",
    description=(
        "Obtiene las comunidades registradas en el sistema.\n\n"
        "- Si **NO** se envía el parámetro `id`, retorna el listado paginado de comunidades.\n"
        "- Si se envía el parámetro `id`, retorna el detalle de una comunidad específica con sus canales.\n\n"
        "El parámetro `id` se envía como **query param**, no como path."
    ),
    parameters=[
        OpenApiParameter(
            name="id",
            description="ID UUID de la comunidad a consultar",
            required=False,
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="is_public",
            description="Filtrar por comunidades públicas o privadas",
            required=False,
            type=OpenApiTypes.BOOL,
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
            description="Cantidad de resultados por página (default = 10)",
            required=False,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
        ),
    ],
    responses={
        200: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            name="Listado de comunidades",
            summary="Respuesta cuando no se envía ID",
            value={
                "count": 2,
                "page": 1,
                "page_size": 10,
                "results": [
                    {
                        "id": "a12f8400-e29b-41d4-a716-446655440111",
                        "name": "Aventureros de Bogotá",
                        "description": "Comunidad para amantes de la aventura",
                        "image": "https://example.com/image.jpg",
                        "company": "Adventure Co.",
                        "location": "Bogotá",
                        "is_public": True,
                        "created_at": "2025-01-15T10:00:00Z",
                        "member_count": 45,
                        "user_is_member": True,
                    },
                    {
                        "id": "b33e8400-e29b-41d4-a716-446655440222",
                        "name": "Senderistas Medellín",
                        "description": "Grupo de senderismo",
                        "image": "https://example.com/image2.jpg",
                        "company": None,
                        "location": "Medellín",
                        "is_public": True,
                        "created_at": "2025-01-10T08:00:00Z",
                        "member_count": 32,
                        "user_is_member": False,
                    }
                ]
            },
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            name="Detalle de comunidad",
            summary="Respuesta cuando se envía ID",
            value={
                "id": "a12f8400-e29b-41d4-a716-446655440111",
                "name": "Aventureros de Bogotá",
                "description": "Comunidad para amantes de la aventura",
                "image": "https://example.com/image.jpg",
                "company": "Adventure Co.",
                "location": "Bogotá",
                "is_public": True,
                "created_at": "2025-01-15T10:00:00Z",
                "member_count": 45,
                "user_is_member": True,
                "canales": [
                    {
                        "id": "c44e8400-e29b-41d4-a716-446655440333",
                        "name": "general",
                        "description": "Canal general",
                        "is_info": False,
                        "is_read_only": False,
                        "created_at": "2025-01-15T10:05:00Z",
                        "post_count": 15,
                    }
                ],
                "created_by_name": "Juan Pérez",
            },
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            name="Comunidad no encontrada",
            value={"detail": "Comunidad no encontrada"},
            response_only=True,
            status_codes=["404"],
        ),
        OpenApiExample(
            name="Parámetros inválidos",
            value={"detail": "page y page_size deben ser enteros positivos"},
            response_only=True,
            status_codes=["400"],
        ),
    ],
)