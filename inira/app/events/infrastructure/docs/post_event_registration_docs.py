# inira/app/events/infrastructure/docs/post_event_registration_docs.py

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes


post_event_registration_docs = extend_schema(
    tags=["Eventos"],
    summary="Inscribirse a un evento",
    description=(
        "Permite que un **usuario autenticado** se inscriba a un evento.\n\n"
        "Validaciones:\n"
        "- El evento debe existir\n"
        "- El usuario no puede estar inscrito previamente\n"
        "- El evento no debe haber alcanzado el máximo de participantes\n\n"
        "🔒 **Requiere autenticación (JWT / Session)**"
    ),
    request=OpenApiTypes.OBJECT,
    responses={
        201: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
        401: OpenApiTypes.OBJECT,
        409: OpenApiTypes.OBJECT,
    },
    examples=[
        # 🔹 REQUEST
        OpenApiExample(
            name="Inscripción exitosa - Request",
            summary="Body requerido para inscribirse",
            value={
                "event_id": "a12f8400-e29b-41d4-a716-446655440111"
            },
            request_only=True,
        ),

        # 🔹 RESPONSE 201
        OpenApiExample(
            name="Inscripción exitosa",
            value={
                "detail": "Inscripción exitosa"
            },
            response_only=True,
            status_codes=["201"],
        ),

        # 🔹 ERROR 400
        OpenApiExample(
            name="Datos inválidos",
            value={
                "detail": "event_id es requerido"
            },
            response_only=True,
            status_codes=["400"],
        ),

        # 🔹 ERROR 401
        OpenApiExample(
            name="No autenticado",
            value={
                "detail": "Authentication credentials were not provided."
            },
            response_only=True,
            status_codes=["401"],
        ),

        # 🔹 ERROR 409
        OpenApiExample(
            name="Ya inscrito o evento lleno",
            value={
                "detail": "Ya estás inscrito en este evento"
            },
            response_only=True,
            status_codes=["409"],
        ),
    ],
)
