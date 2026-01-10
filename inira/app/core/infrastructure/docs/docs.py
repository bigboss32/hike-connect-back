from drf_spectacular.utils import (
    extend_schema, 
    OpenApiParameter, 
    OpenApiResponse,
    OpenApiExample
)
from drf_spectacular.types import OpenApiTypes
from ..out.curso_get_response_serializer import CursoGetResponseSerializer
from ..out.curso_delete_response_serializer import CursoDeleteResponseSerializer
from ..out.curso_create_response_serializer import CursoGoogleResponseSerializer


def core_api_post_schema():
    """
    Schema principal para el endpoint CoreAPIView.
    Documenta todas las operaciones disponibles mediante wsfunction.
    """
    return extend_schema(
        operation_id="execute_moodle_function",
        summary="Ejecutar operaciones de Post",
        description=(
            "Endpoint unificado que ejecuta diferentes operaciones según el parámetro `wsfunction`.\n\n"
            "**Operaciones disponibles:**\n"
            "- `core_course_create_courses`: Crear cursos\n"
            "- `core_course_get_courses`: Obtener cursos\n"
            "- `core_course_update_courses`: Actualizar cursos\n"
            "- `core_course_delete_courses`: Eliminar cursos\n"
            "- `enrol_manual_enrol_users`: Matricular usuarios en cursos\n"
            "- `enrol_manual_unenrol_users`: Desmatricular usuarios de cursos\n\n"
            "Los parámetros adicionales dependen de la operación seleccionada. "
            "Ver ejemplos en la sección de responses."
        ),
        tags=["Core API"],
        parameters=[
            OpenApiParameter(
                name="wstoken",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Token de autenticación de Moodle",
                required=True,
                examples=[
                    OpenApiExample(
                        name="Token ejemplo",
                        value="abc123def456"
                    )
                ]
            ),
            OpenApiParameter(
                name="wsfunction",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    "Función del web service a ejecutar. Determina qué operación se realizará "
                    "y qué parámetros adicionales son requeridos."
                ),
                required=True,
                enum=[
                    "core_course_create_courses",
                    "core_course_get_courses",
                    "core_course_update_courses",
                    "core_course_delete_courses",
                    "enrol_manual_enrol_users",
                    "enrol_manual_unenrol_users",
                    "core_user_create_users"
                ]
            ),
            OpenApiParameter(
                name="moodlewsrestformat",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Formato de respuesta (json, xml)",
                required=False,
                enum=["json", "xml"]
            ),
        ],
        responses={
            200: OpenApiResponse(
                description=(
                    "Operación exitosa. La estructura de respuesta depende de wsfunction:\n\n"
                    "**create_courses**: Retorna el curso creado con su ID\n"
                    "**get_courses**: Retorna lista de cursos\n"
                    "**update_courses**: Retorna confirmación de actualización\n"
                    "**delete_courses**: Retorna confirmación de eliminación\n"
                    "**enrol_manual_enrol_users**: Retorna confirmación de matriculación\n"
                    "**enrol_manual_unenrol_users**: Retorna confirmación de desmatriculación"
                )
            ),
            400: OpenApiResponse(
                description="Parámetros inválidos o wsfunction no soportado"
            ),
            404: OpenApiResponse(
                description="Recurso no encontrado (para operaciones get, update, delete)"
            ),
        },
        examples=[
            OpenApiExample(
                name="Crear curso",
                description="Ejemplo de creación de curso",
                value={
                    "wstoken": "abc123",
                    "wsfunction": "core_course_create_courses",
                    "courses[0][fullname]": "Matemáticas Avanzadas",
                    "courses[0][shortname]": "MAT-ADV",
                    "courses[0][categoryid]": "1"
                }
            ),
            OpenApiExample(
                name="Obtener cursos",
                description="Ejemplo de consulta de cursos",
                value={
                    "wstoken": "abc123",
                    "wsfunction": "core_course_get_courses",
                    "options[ids][0]": "123"
                }
            ),
            OpenApiExample(
                name="Matricular usuario",
                description="Ejemplo de matriculación de usuario en un curso",
                value={
                    "wstoken": "abc123",
                    "wsfunction": "enrol_manual_enrol_users",
                    "enrolments[0][roleid]": "5",
                    "enrolments[0][userid]": "42",
                    "enrolments[0][courseid]": "123"
                }
            ),
            OpenApiExample(
                name="Desmatricular usuario",
                description="Ejemplo de desmatriculación de usuario de un curso",
                value={
                    "wstoken": "abc123",
                    "wsfunction": "enrol_manual_unenrol_users",
                    "enrolments[0][userid]": "42",
                    "enrolments[0][courseid]": "123"
                }
            )
        ]
    )



def core_api_get_schema():
    """
    Schema principal para el endpoint CoreAPIView.
    Documenta todas las operaciones disponibles mediante wsfunction.
    """
    return extend_schema(
        operation_id="execute_moodle_function",
        summary="Ejecutar operaciones de Get",
        description=(
            "Endpoint unificado que ejecuta diferentes operaciones según el parámetro `wsfunction`.\n\n"
            "**Operaciones disponibles:**\n"
            "- `core_course_get_courses`: Obtener cursos\n\n"
            "Los parámetros adicionales dependen de la operación seleccionada. "
            "Ver ejemplos en la sección de responses."
        ),
        tags=["Core API"],
        parameters=[
            OpenApiParameter(
                name="wstoken",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Token de autenticación de Moodle",
                required=True,
                examples=[
                    OpenApiExample(
                        name="Token ejemplo",
                        value="abc123def456"
                    )
                ]
            ),
            OpenApiParameter(
                name="wsfunction",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    "Función del web service a ejecutar. Determina qué operación se realizará "
                    "y qué parámetros adicionales son requeridos."
                ),
                required=True,
                enum=[
                    "core_course_get_courses",
                ]
            ),
            OpenApiParameter(
                name="moodlewsrestformat",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Formato de respuesta (json, xml)",
                required=False,
                enum=["json", "xml"]
            ),
        ],
        responses={
            200: OpenApiResponse(
                description=(
                    "Operación exitosa. La estructura de respuesta depende de wsfunction:\n\n"
                    "**get_courses**: Retorna lista de cursos\n"
                )
            ),
            400: OpenApiResponse(
                description="Parámetros inválidos o wsfunction no soportado"
            ),
            404: OpenApiResponse(
                description="Recurso no encontrado (para operaciones get, update, delete)"
            ),
        },
        examples=[
            OpenApiExample(
                name="Crear curso",
                description="Ejemplo de creación de curso",
                value={
                    "wstoken": "abc123",
                    "wsfunction": "core_course_create_courses",
                    "courses[0][fullname]": "Matemáticas Avanzadas",
                    "courses[0][shortname]": "MAT-ADV",
                    "courses[0][categoryid]": "1"
                }
            ),
            OpenApiExample(
                name="Obtener cursos",
                description="Ejemplo de consulta de cursos",
                value={
                    "wstoken": "abc123",
                    "wsfunction": "core_course_get_courses",
                    "options[ids][0]": "123"
                }
            ),
            OpenApiExample(
                name="Matricular usuario",
                description="Ejemplo de matriculación de usuario en un curso",
                value={
                    "wstoken": "abc123",
                    "wsfunction": "enrol_manual_enrol_users",
                    "enrolments[0][roleid]": "5",
                    "enrolments[0][userid]": "42",
                    "enrolments[0][courseid]": "123"
                }
            ),
            OpenApiExample(
                name="Desmatricular usuario",
                description="Ejemplo de desmatriculación de usuario de un curso",
                value={
                    "wstoken": "abc123",
                    "wsfunction": "enrol_manual_unenrol_users",
                    "enrolments[0][userid]": "42",
                    "enrolments[0][courseid]": "123"
                }
            )
        ]
    )