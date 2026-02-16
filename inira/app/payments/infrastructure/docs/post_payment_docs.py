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
    summary="Procesar pago con Wompi (PSE)",
    description=(
        "Procesa un pago mediante PSE (Proveedor de Servicios Electrónicos) usando Wompi.\n\n"
        "**Flujo del proceso:**\n"
        "1. El usuario envía los datos de pago incluyendo el monto y su información bancaria\n"
        "2. Se crea la transacción en Wompi y se genera una URL de pago\n"
        "3. Se guarda el registro del pago en la base de datos con estado `PENDING`\n"
        "4. Se retorna la información de la transacción y la URL para completar el pago\n"
        "5. **El frontend debe:**\n"
        "   - Redirigir al usuario a la `redirect_url` para que complete el pago en su banco\n"
        "   - Iniciar un **polling** usando GET `/api/v1/payments/{payment_id}/status/` cada 3-5 segundos\n"
        "   - Detener el polling cuando el estado cambie a `APPROVED`, `DECLINED`, o `ERROR`\n"
        "   - Implementar un timeout máximo de 5 minutos\n\n"
        "**Importante:**\n"
        "- El usuario debe estar autenticado (token requerido)\n"
        "- La URL de redirección (`redirect_url`) es donde el usuario completa el pago\n"
        "- El estado inicial del pago será `PENDING`\n"
        "- Usar el endpoint GET `/api/v1/payments/{payment_id}/status/` para verificar el estado\n\n"
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
        # 🔹 REQUEST EJEMPLO
        OpenApiExample(
            name="Request de pago",
            summary="Datos necesarios para procesar un pago PSE",
            value={
                "amount_in_cents": 50000,
                "user_legal_id": "1099888777",
                "user_legal_id_type": "CC",
                "financial_institution_code": "1007",
                "user_type": 0,
                "phone_number": "573107650926",
                "full_name": "Miguel Garzon",
            },
            request_only=True,
        ),
        # 🔹 RESPUESTA EXITOSA
        OpenApiExample(
            name="Pago creado exitosamente",
            summary="Respuesta cuando el pago se procesa correctamente",
            value={
                "payment_id": 123,
                "transaction_id": "12032750-1771217854-91203",
                "status": "PENDING",
                "redirect_url": "https://api-sandbox.wompi.co/v1/pse/redirect?ticket_id=12032750177121785491203",
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
                    "amount_in_cents": ["El monto es requerido"],
                    "user_legal_id": ["La cédula debe contener solo números"],
                    "financial_institution_code": [
                        "El código de la institución financiera es requerido"
                    ],
                }
            },
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
        # 🔹 ERROR - ERROR DEL SERVIDOR
        OpenApiExample(
            name="Error del servidor",
            summary="Error interno al procesar el pago",
            value={"detail": "Error procesando el pago"},
            response_only=True,
            status_codes=["500"],
        ),
    ],
)
