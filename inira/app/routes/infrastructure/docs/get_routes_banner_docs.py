from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes

from inira.app.routes.infrastructure.out.ruta_banner_serializer import (
    RutaBannerSerializer
)


get_routes_banner_docs = extend_schema(
    tags=["Rutas"],
    summary="Obtener rutas para banner",
    description=(
        "Obtiene un listado de rutas optimizadas para mostrar en el **banner principal**.\n\n"
        "Cada ruta incluye únicamente la información necesaria para renderizar el banner:\n"
        "- Imagen\n"
        "- Dificultad\n"
        "- Categoría\n"
        "- Título\n"
        "- Ubicación\n"
        "- Distancia y duración\n"
        "- Rating promedio y número de calificaciones\n\n"
        "Las rutas se retornan ordenadas por fecha de creación (más recientes primero)."
    ),
    responses={
        200: RutaBannerSerializer(many=True),
    },
    examples=[
        OpenApiExample(
            name="Banner de rutas",
            summary="Respuesta exitosa",
            value=[
                {
                    "id": "418d0a33-6c32-4dbc-91c5-c532434fa6b0",
                    "title": "Ruta del Café",
                    "image": "https://cdn.inira.app/rutas/cafe.jpg",
                    "difficulty": "Fácil",
                    "category": "agroturismo",
                    "location": "Eje Cafetero",
                    "distance": "4 km",
                    "duration": "3h",
                    "rating_avg": 4.7,
                    "rating_count": 18
                },
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "title": "Cascada Azul",
                    "image": "https://cdn.inira.app/rutas/cascada.jpg",
                    "difficulty": "Medio",
                    "category": "senderismo",
                    "location": "Antioquia",
                    "distance": "8 km",
                    "duration": "3h",
                    "rating_avg": 4.5,
                    "rating_count": 12
                }
            ],
            response_only=True,
            status_codes=["200"],
        ),
    ],
)
