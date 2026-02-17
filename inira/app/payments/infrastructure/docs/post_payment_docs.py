# inira/app/payments/infrastructure/docs/post_payment_docs.py

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes

from inira.app.payments.infrastructure.input.payment_serializer import (
    ProcessPaymentInputSerializer,
)
from inira.app.payments.infrastructure.out.payment_output_serializer import (
    PaymentOutputSerializer,
)

post_payment_docs = extend_schema(
    tags=["Pagos"],
    summary="Procesar pago con Wompi (PSE) para reserva de ruta",
    description=(
        "Procesa un pago mediante PSE usando Wompi para reservar una ruta de senderismo.\n\n"
        "**Flujo del proceso:**\n"
        "1. El usuario envía los datos de la reserva: ruta, fecha, participantes e información bancaria\n"
        "2. Se valida la disponibilidad de cupos para la fecha seleccionada\n"
        "3. Se calcula el monto total según el precio de la ruta y el número de participantes\n"
        "4. Se crea la transacción en Wompi y se genera una URL de pago\n"
        "5. Se guarda el registro del pago y los participantes con estado `PENDING`\n"
        "6. **El frontend debe:**\n"
        "   - Redirigir al usuario a la `redirect_url` para completar el pago en su banco\n"
        "   - Iniciar un **polling** usando GET `/api/v1/payments/{payment_id}/status/` cada 3-5 segundos\n"
        "   - Detener el polling cuando el estado cambie a `APPROVED`, `DECLINED`, o `ERROR`\n"
        "   - Implementar un timeout máximo de 5 minutos\n\n"
        "**Importante:**\n"
        "- El usuario debe estar autenticado (token requerido)\n"
        "- El primer participante es siempre el titular (quien paga)\n"
        "- El monto se calcula automáticamente: `precio_ruta × número_participantes`\n"
        "- Todos los participantes deben incluir contacto de emergencia\n\n"
        "**Códigos de bancos comunes (financial_institution_code):**\n"
        "- `1007`: Bancolombia\n"
        "- `1019`: Scotiabank Colpatria\n"
        "- `1040`: Banco Agrario\n"
        "- `1052`: Banco AV Villas\n"
        "- `1001`: Banco de Bogotá\n"
        "- `1002`: Banco Popular\n"
    ),
    request=ProcessPaymentInputSerializer,
    responses={
        201: PaymentOutputSerializer,
        400: OpenApiTypes.OBJECT,
        401: OpenApiTypes.OBJECT,
        500: OpenApiTypes.OBJECT,
    },
    examples=[
        # 🔹 REQUEST - UN PARTICIPANTE
        OpenApiExample(
            name="Reserva con un participante",
            summary="Reserva individual (solo el titular)",
            value={
                "ruta_id": "123e4567-e89b-12d3-a456-426614174000",
                "booking_date": "2026-04-15",
                "participants": [
                    {
                        "full_name": "Juan Pérez García",
                        "phone": "+57 300 123 4567",
                        "emergency_contact_name": "María García",
                        "emergency_contact_phone": "+57 301 765 4321",
                    }
                ],
                "user_legal_id": "1099888777",
                "user_legal_id_type": "CC",
                "financial_institution_code": "1007",
                "user_type": 0,
            },
            request_only=True,
        ),
        # 🔹 REQUEST - MÚLTIPLES PARTICIPANTES
        OpenApiExample(
            name="Reserva con múltiples participantes",
            summary="Reserva grupal (titular + acompañantes)",
            value={
                "ruta_id": "123e4567-e89b-12d3-a456-426614174000",
                "booking_date": "2026-04-15",
                "participants": [
                    {
                        "full_name": "Juan Pérez García",
                        "phone": "+57 300 123 4567",
                        "emergency_contact_name": "María García",
                        "emergency_contact_phone": "+57 301 765 4321",
                    },
                    {
                        "full_name": "Ana Martínez López",
                        "phone": "+57 302 987 6543",
                        "emergency_contact_name": "Carlos Martínez",
                        "emergency_contact_phone": "+57 303 456 7890",
                    },
                    {
                        "full_name": "Luis Torres Ruiz",
                        "phone": "+57 304 111 2222",
                        "emergency_contact_name": "Rosa Torres",
                        "emergency_contact_phone": "+57 305 333 4444",
                    },
                ],
                "user_legal_id": "1099888777",
                "user_legal_id_type": "CC",
                "financial_institution_code": "1007",
                "user_type": 0,
            },
            request_only=True,
        ),
        # 🔹 RESPUESTA EXITOSA
        OpenApiExample(
            name="Reserva creada exitosamente",
            summary="Respuesta cuando la reserva y el pago se procesan correctamente",
            value={
                "payment_id": "550e8400-e29b-41d4-a716-446655440000",
                "transaction_id": "12032750-1771217854-91203",
                "status": "PENDING",
                "redirect_url": "https://api-sandbox.wompi.co/v1/pse/redirect?ticket_id=12032750177121785491203",
                "ruta_id": "123e4567-e89b-12d3-a456-426614174000",
                "booking_date": "2026-04-15",
                "total_participants": 3,
                "amount": "255000.00",
            },
            response_only=True,
            status_codes=["201"],
        ),
        # 🔹 ERROR - VALIDACIÓN DE DATOS
        OpenApiExample(
            name="Error de validación",
            summary="Cuando faltan campos requeridos o son inválidos",
            value={
                "errors": {
                    "ruta_id": ["Este campo es requerido"],
                    "booking_date": ["La fecha de la excursión debe ser futura"],
                    "participants": ["Debe agregar al menos un participante"],
                    "financial_institution_code": ["Este campo es requerido"],
                }
            },
            response_only=True,
            status_codes=["400"],
        ),
        # 🔹 ERROR - SIN CUPOS
        OpenApiExample(
            name="Sin cupos disponibles",
            summary="Cuando no hay cupos para la fecha seleccionada",
            value={"detail": "Solo quedan 2 cupos disponibles"},
            response_only=True,
            status_codes=["400"],
        ),
        # 🔹 ERROR - RUTA INACTIVA
        OpenApiExample(
            name="Ruta no disponible",
            summary="Cuando la ruta no está activa",
            value={"detail": "Esta ruta no está disponible actualmente"},
            response_only=True,
            status_codes=["400"],
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
            summary="Error interno al procesar el pago",
            value={"detail": "Error procesando el pago"},
            response_only=True,
            status_codes=["500"],
        ),
    ],
)
