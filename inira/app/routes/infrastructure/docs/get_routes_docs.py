from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes

from inira.app.routes.infrastructure.out.route_output_serializer import (
    RouteOutputSerializer
)


get_routes_docs = extend_schema(
    tags=["Rutas"],
    summary="Obtener rutas de senderismo",
    description=(
        "Obtiene rutas de senderismo registradas en el sistema.\n\n"
        "- Si **NO** se envía el parámetro `id`, retorna el listado completo.\n"
        "- Si se envía el parámetro `id`, retorna una ruta específica.\n\n"
        "El parámetro `id` se envía como **query param**, no como path."
    ),
    parameters=[
        OpenApiParameter(
            name="id",
            description="ID UUID de la ruta a consultar",
            required=False,
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="difficulty",
            description="Filtrar por dificultad (Fácil, Medio, Difícil)",
            required=False,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="category",
            description="Filtrar por categoría (senderismo, agroturismo)",
            required=False,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
        ),
    ],
    responses={
        200: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    examples=[
        # 🔹 LISTADO
        OpenApiExample(
            name="Listado de rutas",
            summary="Respuesta cuando no se envía ID",
            value={
                "count": 2,
                "results": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "Ruta Cascada Azul",
                        "location": "Antioquia",
                        "distance": "8 km",
                        "duration": "3h",
                        "difficulty": "Fácil",
                        "image": "https://example.com/image.jpg",
                        "type": "pública",
                        "category": "senderismo",
                        "description": "Hermosa ruta natural",
                        "company": None,
                        "phone": "3001234567",
                        "email": "info@ruta.com",
                        "whatsapp": "3001234567",
                        "coordinates": {
                            "lat": 6.25184,
                            "lng": -75.56359
                        },
                        "created_at": "2025-01-01T10:00:00Z",
                        "updated_at": "2025-01-01T10:00:00Z"
                    }
                ]
            },
            response_only=True,
            status_codes=["200"],
        ),

        # 🔹 UNA RUTA
        OpenApiExample(
            name="Detalle de ruta",
            summary="Respuesta cuando se envía ID",
            value={
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Ruta Cascada Azul",
                "location": "Antioquia",
                "distance": "8 km",
                "duration": "3h",
                "difficulty": "Fácil",
                "image": "https://example.com/image.jpg",
                "type": "pública",
                "category": "senderismo",
                "description": "Hermosa ruta natural",
                "company": None,
                "phone": "3001234567",
                "email": "info@ruta.com",
                "whatsapp": "3001234567",
                "coordinates": {
                    "lat": 6.25184,
                    "lng": -75.56359
                },
                "created_at": "2025-01-01T10:00:00Z",
                "updated_at": "2025-01-01T10:00:00Z"
            },
            response_only=True,
            status_codes=["200"],
        ),

        # 🔹 ERROR 404
        OpenApiExample(
            name="Ruta no encontrada",
            value={
                "detail": "No existe una ruta con id ..."
            },
            response_only=True,
            status_codes=["404"],
        ),

        # 🔹 ERROR 400
        OpenApiExample(
            name="UUID inválido",
            value={
                "id": ["Must be a valid UUID."]
            },
            response_only=True,
            status_codes=["400"],
        ),
    ],
)
