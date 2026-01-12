from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from inira.app.accounts.infrastructure.input.register_input_serializer import RegisterInputSerializer
from inira.app.accounts.infrastructure.out.login_output_serializer import LoginOutputSerializer


register_docs = extend_schema(
    tags=["Autenticación"],
    summary="Registrar nuevo usuario",
    description=(
        "Crea una nueva cuenta de usuario en el sistema. "
        "El email se utiliza como nombre de usuario. "
        "Retorna tokens JWT de acceso y actualización para el usuario recién creado."
    ),
    request=RegisterInputSerializer,
    responses={
        201: LoginOutputSerializer,
        400: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            "Registro exitoso",
            value={
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "user": {
                    "id": 2,
                    "email": "nuevo@ejemplo.com",
                    "first_name": "Juan",
                    "last_name": "Pérez",
                    "full_name": "Juan Pérez"
                },
            },
            response_only=True,
            status_codes=['201'],
        ),
        OpenApiExample(
            "Datos de entrada",
            value={
                "email": "nuevo@ejemplo.com",
                "password": "MiPassword123!",
                "password_confirm": "MiPassword123!",
                "first_name": "Juan",
                "last_name": "Pérez"
            },
            request_only=True,
        ),
        OpenApiExample(
            "Email ya registrado",
            value={
                "email": ["Este email ya está registrado"]
            },
            response_only=True,
            status_codes=['400'],
        ),
        OpenApiExample(
            "Contraseñas no coinciden",
            value={
                "password_confirm": ["Las contraseñas no coinciden"]
            },
            response_only=True,
            status_codes=['400'],
        ),
    ],
)