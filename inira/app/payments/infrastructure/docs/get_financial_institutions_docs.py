# inira/app/payments/infrastructure/docs/get_financial_institutions_docs.py

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes

get_financial_institutions_docs = extend_schema(
    tags=["Pagos"],
    summary="Obtener instituciones financieras disponibles para PSE",
    description=(
        "Retorna la lista de bancos e instituciones financieras disponibles para realizar pagos mediante PSE.\n\n"
        "**Uso recomendado:**\n"
        "- Llamar este endpoint al cargar el formulario de pago\n"
        "- Mostrar la lista en un selector para que el usuario elija su banco\n"
        "- Usar el `financial_institution_code` retornado en el campo `financial_institution_code` "
        "del endpoint de creación de pago (`POST /api/v1/payments/`)\n\n"
        "**Importante:**\n"
        "- El usuario debe estar autenticado (token requerido)\n"
        "- Los datos provienen directamente de la API de Wompi en tiempo real\n"
    ),
    responses={
        200: OpenApiTypes.OBJECT,
        401: OpenApiTypes.OBJECT,
        500: OpenApiTypes.OBJECT,
    },
    examples=[
        # 🔹 RESPUESTA EXITOSA
        OpenApiExample(
            name="Lista de instituciones financieras",
            summary="Respuesta con los bancos disponibles para PSE",
            value={
                "data": [
                    {
                        "financial_institution_code": "1007",
                        "financial_institution_name": "BANCOLOMBIA",
                    },
                    {
                        "financial_institution_code": "1001",
                        "financial_institution_name": "BANCO DE BOGOTA",
                    },
                    {
                        "financial_institution_code": "1002",
                        "financial_institution_name": "BANCO POPULAR",
                    },
                    {
                        "financial_institution_code": "1019",
                        "financial_institution_name": "SCOTIABANK COLPATRIA",
                    },
                    {
                        "financial_institution_code": "1040",
                        "financial_institution_name": "BANCO AGRARIO",
                    },
                    {
                        "financial_institution_code": "1052",
                        "financial_institution_name": "BANCO AV VILLAS",
                    },
                ]
            },
            response_only=True,
            status_codes=["200"],
        ),
        # 🔹 ERROR - NO AUTENTICADO
        OpenApiExample(
            name="No autenticado",
            summary="Cuando no se envía el token de autenticación",
            value={"detail": "Las credenciales de autenticación no se proveyeron."},
            response_only=True,
            status_codes=["401"],
        ),
        # 🔹 ERROR - SERVIDOR
        OpenApiExample(
            name="Error del servidor",
            summary="Error interno al obtener las instituciones financieras",
            value={"detail": "Error obteniendo instituciones financieras"},
            response_only=True,
            status_codes=["500"],
        ),
    ],
)
