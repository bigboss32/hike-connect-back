# inira/app/accounts/infrastructure/docs/resend_verification_docs.py

from drf_spectacular.utils import extend_schema

from inira.app.accounts.infrastructure.input.resend_verification_serializer import (
    ResendVerificationSerializer,
)


resend_verification_docs = extend_schema(
    tags=["Autenticación"],
    summary="Reenviar código de verificación",
    description=(
        "Reenvía un nuevo código de verificación al correo del usuario "
        "si la cuenta aún no ha sido activada."
    ),
    request=ResendVerificationSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
            },
            "example": {"message": "Código reenviado correctamente"},
        },
        400: {
            "type": "object",
            "properties": {
                "detail": {"type": "string"},
            },
            "example": {"detail": "No hay verificación pendiente."},
        },
    },
)
