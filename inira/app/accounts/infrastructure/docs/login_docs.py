from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from inira.app.accounts.infrastructure.input.login_input_serializer import LoginInputSerializer
from inira.app.accounts.infrastructure.out.login_output_serializer import LoginOutputSerializer


login_docs = extend_schema(
    tags=["Autenticación"],
    summary="Iniciar sesión",
    description=(
        "Autentica un usuario mediante email y contraseña, "
        "retornando tokens JWT de acceso y actualización."
    ),
    request=LoginInputSerializer,
    responses={
        200: LoginOutputSerializer,
        400: OpenApiTypes.OBJECT,
        401: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            "Login exitoso",
            value={
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "user": {
                    "id": 1,
                    "email": "usuario@ejemplo.com",
                    "name": "Juan Pérez",
                },
            },
            response_only=True,
            status_codes=['200'],
        ),
        OpenApiExample(
            "Credenciales inválidas",
            value={
                "detail": ["Credenciales inválidas"]
            },
            response_only=True,
            status_codes=['400'],
        ),
        OpenApiExample(
            "Usuario inactivo",
            value={
                "detail": ["Usuario inactivo"]
            },
            response_only=True,
            status_codes=['401'],
        ),
    ],
)