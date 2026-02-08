# verify_email_docs.py

from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from inira.app.accounts.infrastructure.input.verify_email_serializer import (
    VerifyEmailSerializer,
)


verify_email_docs = extend_schema(
    tags=["Autenticación"],
    summary="Verificar correo electrónico",
    description=(
        "Verifica el correo electrónico del usuario mediante un código de verificación "
        "enviado previamente. El código tiene una validez de 10 minutos. "
        "Una vez verificado, el campo correo_electronico_confirmado se actualiza a True."
    ),
    request=VerifyEmailSerializer,
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            "Verificación exitosa",
            value={"message": "Correo verificado correctamente"},
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Datos de entrada",
            value={
                "email": "usuario@ejemplo.com",
                "code": "123456",
            },
            request_only=True,
        ),
        OpenApiExample(
            "Código inválido",
            value={"detail": "Código inválido"},
            response_only=True,
            status_codes=["400"],
        ),
        OpenApiExample(
            "Código expirado",
            value={"detail": "Código expirado. Solicita uno nuevo."},
            response_only=True,
            status_codes=["400"],
        ),
    ],
)
