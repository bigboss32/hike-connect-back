# inira/app/payments/infrastructure/docs/get_payment_status_docs.py

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes

from inira.app.payments.infrastructure.out.payment_output_serializer import (
    PaymentStatusOutputSerializer,
)


get_payment_status_docs = extend_schema(
    tags=["Pagos"],
    summary="Consultar estado de un pago",
    description=(
        "Consulta el estado actual de una transacción de pago en Wompi.\n\n"
        "**Flujo de uso:**\n"
        "1. Después de crear un pago con POST `/api/v1/payments/`, recibirás un `payment_id` y una `redirect_url`\n"
        "2. Redirige al usuario a la `redirect_url` para que complete el pago en su banco\n"
        "3. Usa este endpoint para hacer **polling** (consultar periódicamente) el estado del pago\n"
        "4. El polling debe hacerse cada 3-5 segundos hasta que el estado cambie a `APPROVED`, `DECLINED`, o `ERROR`\n\n"
        "**Estados posibles:**\n"
        "- `PENDING`: Pago pendiente de confirmación\n"
        "- `APPROVED`: Pago aprobado exitosamente\n"
        "- `DECLINED`: Pago rechazado\n"
        "- `VOIDED`: Pago anulado\n"
        "- `ERROR`: Error en el procesamiento\n\n"
        "**Importante:**\n"
        "- Solo puedes consultar pagos que pertenezcan a tu usuario autenticado\n"
        "- El estado se actualiza automáticamente consultando desde Wompi\n"
        "- El monto se retorna en COP (no en centavos)\n"
        "- Se recomienda implementar un timeout máximo de 5 minutos para el polling\n"
    ),
    parameters=[
        OpenApiParameter(
            name="payment_id",
            description="UUID del pago a consultar",
            required=True,
            type=OpenApiTypes.UUID,  # 🔹 Cambiado de INT a UUID
            location=OpenApiParameter.PATH,
        ),
    ],
    responses={
        200: PaymentStatusOutputSerializer,
        401: OpenApiTypes.OBJECT,
        403: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
        500: OpenApiTypes.OBJECT,
    },
    examples=[
        # 🔹 ESTADO PENDIENTE
        OpenApiExample(
            name="Estado: Pendiente",
            summary="Pago pendiente de confirmación del banco",
            value={
                "payment_id": "550e8400-e29b-41d4-a716-446655440000",
                "transaction_id": "12032750-1771217854-91203",
                "status": "PENDING",
                "amount": "255000.00",  # 🔹 COP no centavos
                "reference": "PAY_USER_3_1771217766",
                "redirect_url": "https://api-sandbox.wompi.co/v1/pse/redirect?ticket_id=12032750177121785491203",
                "ticket_id": "12032750177121785491203",
                "return_code": "SUCCESS",
                "ruta_id": "123e4567-e89b-12d3-a456-426614174000",  # 🆕
                "booking_date": "2026-04-15",  # 🆕
                "total_participants": 3,  # 🆕
                "created_at": "2026-02-16T04:56:06.123456Z",
                "updated_at": "2026-02-16T04:56:06.123456Z",
            },
            response_only=True,
            status_codes=["200"],
        ),
        # 🔹 ESTADO APROBADO
        OpenApiExample(
            name="Estado: Aprobado",
            summary="Pago aprobado exitosamente",
            value={
                "payment_id": "550e8400-e29b-41d4-a716-446655440000",
                "transaction_id": "12032750-1771217854-91203",
                "status": "APPROVED",
                "amount": "255000.00",
                "reference": "PAY_USER_3_1771217766",
                "redirect_url": "https://api-sandbox.wompi.co/v1/pse/redirect?ticket_id=12032750177121785491203",
                "ticket_id": "12032750177121785491203",
                "return_code": "SUCCESS",
                "ruta_id": "123e4567-e89b-12d3-a456-426614174000",
                "booking_date": "2026-04-15",
                "total_participants": 3,
                "created_at": "2026-02-16T04:56:06.123456Z",
                "updated_at": "2026-02-16T05:01:23.789012Z",
            },
            response_only=True,
            status_codes=["200"],
        ),
        # 🔹 ESTADO RECHAZADO
        OpenApiExample(
            name="Estado: Rechazado",
            summary="Pago rechazado por el banco",
            value={
                "payment_id": "550e8400-e29b-41d4-a716-446655440000",
                "transaction_id": "12032750-1771217854-91203",
                "status": "DECLINED",
                "amount": "255000.00",
                "reference": "PAY_USER_3_1771217766",
                "redirect_url": "https://api-sandbox.wompi.co/v1/pse/redirect?ticket_id=12032750177121785491203",
                "ticket_id": "12032750177121785491203",
                "return_code": "FAILED",
                "ruta_id": "123e4567-e89b-12d3-a456-426614174000",
                "booking_date": "2026-04-15",
                "total_participants": 3,
                "created_at": "2026-02-16T04:56:06.123456Z",
                "updated_at": "2026-02-16T05:00:15.456789Z",
            },
            response_only=True,
            status_codes=["200"],
        ),
        # 🔹 ERROR - PAGO NO ENCONTRADO
        OpenApiExample(
            name="Pago no encontrado",
            summary="El payment_id no existe",
            value={"detail": "Pago no encontrado"},
            response_only=True,
            status_codes=["404"],
        ),
        # 🔹 ERROR - SIN PERMISOS
        OpenApiExample(
            name="Sin permisos",
            summary="Intentando acceder a un pago de otro usuario",
            value={"detail": "No tiene permisos para acceder a este pago"},
            response_only=True,
            status_codes=["403"],
        ),
        # 🔹 ERROR - NO AUTENTICADO
        OpenApiExample(
            name="No autenticado",
            summary="Token de autenticación no proporcionado o inválido",
            value={"detail": "Las credenciales de autenticación no se proveyeron."},
            response_only=True,
            status_codes=["401"],
        ),
        # 🔹 ERROR DEL SERVIDOR
        OpenApiExample(
            name="Error del servidor",
            summary="Error al consultar el estado en Wompi",
            value={"detail": "Error al consultar estado del pago"},
            response_only=True,
            status_codes=["500"],
        ),
    ],
)
