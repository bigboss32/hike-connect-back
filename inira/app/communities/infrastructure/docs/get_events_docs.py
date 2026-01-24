# inira/app/events/infrastructure/docs/get_events_docs.py

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes


get_events_docs = extend_schema(
    tags=["Eventos"],
    summary="Obtener eventos",
    description=(
        "Obtiene los eventos registrados en el sistema.\n\n"
        "- Si **NO** se envía el parámetro `id`, retorna el listado paginado de eventos.\n"
        "- Si se envía el parámetro `id`, retorna el detalle de un evento específico.\n\n"
        "El parámetro `id` se envía como **query param**, no como path."
    ),
    parameters=[
        OpenApiParameter(
            name="id",
            description="ID UUID del evento a consultar",
            required=False,
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
        # 🔹 LISTADO DE EVENTOS
        OpenApiExample(
            name="Listado de eventos",
            summary="Respuesta cuando no se envía ID",
            value={
                "count": 2,
                "page": 1,
                "page_size": 10,
                "results": [
                    {
                        "id": "a12f8400-e29b-41d4-a716-446655440111",
                        "title": "Senderismo al Nevado",
                        "date": "2025-10-15T08:00:00Z",
                        "location": "Sierra Nevada",
                        "max_participants": 15,
                    },
                    {
                        "id": "b33e8400-e29b-41d4-a716-446655440222",
                        "title": "Caminata Nocturna",
                        "date": "2025-11-02T19:00:00Z",
                        "location": "Bogotá",
                        "max_participants": 20,
                    }
                ]
            },
            response_only=True,
            status_codes=["200"],
        ),

        # 🔹 DETALLE DE EVENTO
        OpenApiExample(
            name="Detalle de evento",
            summary="Respuesta cuando se envía ID",
            value={
                "id": "a12f8400-e29b-41d4-a716-446655440111",
                "title": "Senderismo al Nevado",
                "date": "2025-10-15T08:00:00Z",
                "location": "Sierra Nevada",
                "max_participants": 15,
            },
            response_only=True,
            status_codes=["200"],
        ),

        # 🔹 ERROR 404
        OpenApiExample(
            name="Evento no encontrado",
            value={
                "detail": "Evento no encontrado"
            },
            response_only=True,
            status_codes=["404"],
        ),

        # 🔹 ERROR 400
        OpenApiExample(
            name="Parámetros inválidos",
            value={
                "detail": "page y page_size deben ser enteros positivos"
            },
            response_only=True,
            status_codes=["400"],
        ),
    ],
)
