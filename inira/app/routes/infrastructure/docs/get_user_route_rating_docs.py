from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)
from rest_framework import status


get_user_route_rating_docs = extend_schema(
    tags=["Rutas"],
    summary="Obtener calificación del usuario y estadísticas de la ruta",
    description=(
        "Devuelve la calificación del usuario autenticado para una ruta "
        "junto con el promedio y la cantidad total de calificaciones."
    ),
    parameters=[
        OpenApiParameter(
            name="ruta_id",
            description="ID de la ruta de senderismo",
            required=True,
            type=str,
            location=OpenApiParameter.QUERY,
        ),
    ],
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="Calificación y estadísticas",
            response={
                "type": "object",
                "properties": {
                    "score": {
                        "type": ["integer", "null"],
                        "example": 4,
                        "description": "Calificación del usuario",
                    },
                    "rating_avg": {
                        "type": ["number", "null"],
                        "example": 4.6,
                        "description": "Promedio de calificaciones",
                    },
                    "rating_count": {
                        "type": "integer",
                        "example": 21,
                        "description": "Total de calificaciones",
                    },
                },
            },
        ),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            description="La ruta no existe",
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            description="Usuario no autenticado",
        ),
    },
)
