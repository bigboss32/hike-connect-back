from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from inira.app.accounts.infrastructure.input.logout_input_serializer import LogoutInputSerializer


logout_docs = extend_schema(
    tags=["Autenticación"],
    summary="Cerrar sesión",
    description=(
        "Invalida el refresh token del usuario para cerrar la sesión. "
        "Una vez invalidado, el refresh token no podrá ser usado para obtener nuevos access tokens. "
        "**Este endpoint NO requiere autenticación**, solo necesita el refresh token en el body."
    ),
    request=LogoutInputSerializer,
    responses={
        205: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    auth=[],  # ← IMPORTANTE: Indica que NO requiere autenticación
    examples=[
        OpenApiExample(
            "Datos de entrada",
            value={
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            },
            request_only=True,
        ),
        OpenApiExample(
            "Logout exitoso",
            value={
                "detail": "Sesión cerrada exitosamente"
            },
            response_only=True,
            status_codes=['205'],
        ),
        OpenApiExample(
            "Token inválido",
            value={
                "detail": "Token inválido o expirado"
            },
            response_only=True,
            status_codes=['400'],
        ),
    ],
)