# inira/app/routes/infrastructure/docs/get_my_routes_docs.py

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from inira.app.routes.infrastructure.out.route_output_serializer import (
    RouteOutputSerializer,
)

get_my_routes_docs = extend_schema(
    tags=["Rutas"],
    summary="Mis rutas",
    description=(
        "Retorna las rutas creadas por el usuario autenticado.\n\n"
        "- Requiere autenticación.\n"
        "- Solo retorna rutas del usuario que hace la petición."
    ),
    parameters=[
        OpenApiParameter(
            name="page",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Número de página (default: 1)",
        ),
        OpenApiParameter(
            name="page_size",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Resultados por página (default: 10)",
        ),
    ],
    responses={200: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            name="Mis rutas",
            value={
                "count": 1,
                "page": 1,
                "page_size": 10,
                "results": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "Ruta Cascada Azul",
                        "location": "Antioquia, Colombia",
                        "distance": "8 km",
                        "duration": "3-4 horas",
                        "difficulty": "Fácil",
                        "image": "https://example.com/imagen.jpg",
                        "type": "pública",
                        "category": "senderismo",
                        "description": "Hermosa ruta.",
                        "coordinates": {"lat": 6.25184, "lng": -75.56359},
                        "company": "Ecoturismo Antioquia SAS",
                        "phone": "3001234567",
                        "email": "info@ruta.com",
                        "whatsapp": "3001234567",
                        "base_price": "45000.00",
                        "requires_payment": True,
                        "max_capacity": 25,
                        "min_participants": 2,
                        "max_participants_per_booking": 8,
                        "requires_date_selection": True,
                        "is_active": True,
                        "included_services": "Guía certificado\nRefrigerio",
                        "requirements": "Buena condición física",
                        "what_to_bring": "Agua\nProtector solar",
                        "rating_avg": 4.5,
                        "rating_count": 12,
                        "created_at": "2025-01-01T10:00:00Z",
                        "updated_at": "2025-01-01T10:00:00Z",
                    }
                ],
            },
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            name="No autenticado",
            value={"detail": "Authentication credentials were not provided."},
            response_only=True,
            status_codes=["401"],
        ),
    ],
)
