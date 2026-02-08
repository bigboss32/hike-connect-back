# inira/app/accounts/infrastructure/docs/password_reset_docs.py

from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from inira.app.accounts.infrastructure.input import (
    RequestPasswordResetSerializer,
    VerifyPasswordResetCodeSerializer,
    ResetPasswordSerializer,
)


request_password_reset_docs = extend_schema(
    tags=["Autenticación"],
    summary="Solicitar recuperación de contraseña",
    description=(
        "Envía un código de 6 dígitos al correo electrónico del usuario "
        "para recuperar su contraseña. El código tiene una validez de 10 minutos."
    ),
    request=RequestPasswordResetSerializer,
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            "Solicitud exitosa",
            value={"message": "Código enviado a tu correo electrónico"},
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Datos de entrada",
            value={"email": "usuario@ejemplo.com"},
            request_only=True,
        ),
        OpenApiExample(
            "Email no encontrado",
            value={"email": ["No existe una cuenta con este correo."]},
            response_only=True,
            status_codes=["400"],
        ),
    ],
)


verify_password_reset_code_docs = extend_schema(
    tags=["Autenticación"],
    summary="Verificar código de recuperación",
    description=(
        "Verifica que el código de recuperación sea válido antes de "
        "permitir al usuario establecer una nueva contraseña."
    ),
    request=VerifyPasswordResetCodeSerializer,
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            "Código válido",
            value={"message": "Código válido"},
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Datos de entrada",
            value={"email": "usuario@ejemplo.com", "code": "123456"},
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


reset_password_docs = extend_schema(
    tags=["Autenticación"],
    summary="Establecer nueva contraseña",
    description=(
        "Establece una nueva contraseña para el usuario después de verificar "
        "el código de recuperación. El código se invalida después de usarse."
    ),
    request=ResetPasswordSerializer,
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            "Contraseña actualizada",
            value={"message": "Contraseña actualizada correctamente"},
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Datos de entrada",
            value={
                "email": "usuario@ejemplo.com",
                "code": "123456",
                "password": "NuevaPassword123!",
                "password_confirm": "NuevaPassword123!",
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
            "Contraseñas no coinciden",
            value={"password_confirm": ["Las contraseñas no coinciden"]},
            response_only=True,
            status_codes=["400"],
        ),
    ],
)
