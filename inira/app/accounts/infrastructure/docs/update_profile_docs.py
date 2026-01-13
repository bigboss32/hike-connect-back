from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from inira.app.accounts.infrastructure.input.update_profile_input_serializer import UpdateProfileInputSerializer
from inira.app.accounts.infrastructure.out.user_output_serializer import UserOutputSerializer


update_profile_docs = extend_schema(
    tags=["Usuarios"],
    summary="Actualizar perfil de usuario",
    description=(
        "Actualiza parcialmente los datos del perfil del usuario autenticado. "
        "Solo es necesario enviar los campos que se desean actualizar."
    ),
    request=UpdateProfileInputSerializer,
    responses={
        200: UserOutputSerializer,
        400: OpenApiTypes.OBJECT,
        401: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            "Actualizar nombre y apellido",
            value={
                "first_name": "Miguel Ángel",
                "last_name": "Garzón S"
            },
            request_only=True,
        ),
        OpenApiExample(
            "Actualizar solo biografía",
            value={
                "bio": "Amante de la naturaleza y el senderismo. Siempre buscando nuevas rutas por descubrir."
            },
            request_only=True,
        ),
        OpenApiExample(
            "Actualización exitosa",
            value={
                "id": 1,
                "email": "admin@local.dev",
                "first_name": "Miguel Ángel",
                "last_name": "Garzón S",
                "full_name": "Miguel Ángel Garzón S",
                "bio": "Amante de la naturaleza y el senderismo. Siempre buscando nuevas rutas por descubrir."
            },
            response_only=True,
            status_codes=['200'],
        ),
        OpenApiExample(
            "Campo vacío",
            value={
                "first_name": ["El nombre no puede estar vacío"]
            },
            response_only=True,
            status_codes=['400'],
        ),
    ],
)

# Para obtener el perfil
get_profile_docs = extend_schema(
    tags=["Usuarios"],
    summary="Obtener perfil de usuario",
    description="Obtiene los datos del perfil del usuario autenticado.",
    responses={
        200: UserOutputSerializer,
        401: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            "Perfil obtenido",
            value={
                "id": 1,
                "email": "admin@local.dev",
                "first_name": "Miguel Ángel",
                "last_name": "Garzón S",
                "full_name": "Miguel Ángel Garzón S",
                "bio": "Amante de la naturaleza y el senderismo."
            },
            response_only=True,
            status_codes=['200'],
        ),
    ],
)