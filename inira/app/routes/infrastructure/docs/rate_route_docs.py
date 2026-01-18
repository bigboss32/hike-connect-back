from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes

from inira.app.routes.infrastructure.input.ruta_rating_serializer import RutaRatingInputSerializer


rate_route_docs = extend_schema(
    tags=["Rutas"],
    summary="Calificar una ruta",
    description=(
        "Permite a un usuario autenticado calificar una ruta de senderismo.\n\n"
        "- El usuario solo puede tener **una calificación por ruta**.\n"
        "- Si ya existe una calificación previa, esta se **actualiza**.\n"
        "- El `ruta_id` y el `score` se envían en el **body**.\n"
        "- El score debe estar entre **1 y 5**."
    ),
    request=RutaRatingInputSerializer,
    responses={
        201: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
        401: OpenApiTypes.OBJECT,
    },
    examples=[
        # ✅ REQUEST
        OpenApiExample(
            name="Calificar ruta",
            summary="Ejemplo de request",
            value={
                "ruta_id": "550e8400-e29b-41d4-a716-446655440000",
                "score": 5
            },
            request_only=True,
        ),

        # ✅ SUCCESS
        OpenApiExample(
            name="Calificación exitosa",
            value={
                "detail": "Ruta calificada correctamente"
            },
            response_only=True,
            status_codes=["201"],
        ),

        # ❌ ERROR 400
        OpenApiExample(
            name="Score inválido",
            value={
                "score": ["Ensure this value is less than or equal to 5."]
            },
            response_only=True,
            status_codes=["400"],
        ),
    ],
)
