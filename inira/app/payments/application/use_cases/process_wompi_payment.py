# inira/app/payments/application/use_cases/process_wompi_payment.py

import logging


from inira.app.payments.domain.services.wompi_services import WompiService
from inira.app.payments.domain.repositories.payment_repository import PaymentRepository

logger = logging.getLogger(__name__)


class ProcessWompiPayment:
    def __init__(
        self,
        wompi_service: WompiService,
        payment_repository: PaymentRepository,
    ):
        self.wompi_service = wompi_service
        self.payment_repository = payment_repository

    def execute(self, payment_data: dict):
        """
        payment_data debe contener:
        - amount_in_cents
        - user_id
        - user_email
        - user_phone
        - user_full_name
        - user_legal_id
        - user_legal_id_type
        - user_type
        - financial_institution_code
        - reference (opcional, se genera automáticamente si no se proporciona)
        """

        user_id = payment_data["user_id"]
        amount = payment_data["amount_in_cents"]

        logger.info(
            f"[INICIO] Procesando pago - User ID: {user_id}, Amount: {amount} COP cents"
        )

        try:
            # Generar referencia si no se proporciona
            reference = (
                payment_data.get("reference")
                or f"PAY_USER_{payment_data['user_id']}_{payment_data.get('timestamp', '')}"
            )

            logger.info(f"[REFERENCIA] Generada: {reference}")

            # 1. Crear la transacción en Wompi
            logger.info(
                f"[WOMPI] Iniciando creación de transacción PSE - "
                f"Reference: {reference}, "
                f"Bank: {payment_data['financial_institution_code']}, "
                f"User: {payment_data['user_full_name']}"
            )

            wompi_response = self.wompi_service.create_pse_transaction(
                amount_in_cents=payment_data["amount_in_cents"],
                reference=reference,
                customer_email=payment_data["user_email"],
                customer_phone=payment_data["user_phone"],
                customer_full_name=payment_data["user_full_name"],
                user_legal_id=payment_data["user_legal_id"],
                user_legal_id_type=payment_data["user_legal_id_type"],
                user_type=payment_data["user_type"],
                financial_institution_code=payment_data["financial_institution_code"],
            )

            transaction_id = wompi_response["data"]["id"]
            transaction_status = wompi_response["data"]["status"]
            redirect_url = (
                wompi_response["data"]
                .get("payment_method", {})
                .get("extra", {})
                .get("async_payment_url")
            )

            logger.info(
                f"[WOMPI] Transacción creada exitosamente - "
                f"Transaction ID: {transaction_id}, "
                f"Status: {transaction_status}, "
                f"Has redirect URL: {bool(redirect_url)}"
            )

            # 2. Guardar el registro del pago
            logger.info(
                f"[DB] Guardando registro del pago en base de datos - "
                f"Reference: {reference}, "
                f"Transaction ID: {transaction_id}"
            )

            payment = self.payment_repository.create(
                user_id=payment_data["user_id"],
                wompi_transaction_id=transaction_id,
                amount_in_cents=payment_data["amount_in_cents"],
                status=transaction_status,
                payment_method_type="PSE",
                reference=reference,
            )

            logger.info(f"[DB] Pago guardado exitosamente - Payment ID: {payment.id}")

            result = {
                "payment_id": payment.id,
                "transaction_id": transaction_id,
                "status": transaction_status,
                "redirect_url": redirect_url,
            }

            logger.info(
                f"[ÉXITO] Pago procesado completamente - "
                f"Payment ID: {payment.id}, "
                f"Transaction ID: {transaction_id}, "
                f"Reference: {reference}"
            )

            return result

        except KeyError as e:
            logger.error(
                f"[ERROR] Datos faltantes en payment_data - "
                f"Campo faltante: {str(e)}, "
                f"User ID: {user_id}"
            )
            raise ValueError(f"Campo requerido faltante: {str(e)}")

        except Exception as e:
            logger.error(
                f"[ERROR] Error inesperado al procesar pago - "
                f"User ID: {user_id}, "
                f"Error: {str(e)}, "
                f"Type: {type(e).__name__}",
                exc_info=True,
            )
            raise
