# inira/app/payments/infrastructure/repositories/payment_repository_impl.py

import logging
from inira.app.payments.domain.repositories.payment_repository import PaymentRepository
from inira.app.payments.infrastructure.models import Payment

logger = logging.getLogger(__name__)


class PaymentRepositoryImpl(PaymentRepository):
    def create(
        self,
        user_id: int,
        wompi_transaction_id: str,
        amount_in_cents: int,
        status: str,
        payment_method_type: str,
        reference: str,
    ):
        try:
            logger.info(
                f"[PAYMENT_REPO] Creando registro - "
                f"User ID: {user_id}, "
                f"Transaction ID: {wompi_transaction_id}, "
                f"Reference: {reference}"
            )

            payment = Payment.objects.create(
                user_id=user_id,
                wompi_transaction_id=wompi_transaction_id,
                amount_in_cents=amount_in_cents,
                status=status,
                payment_method_type=payment_method_type,
                reference=reference,
            )

            logger.info(
                f"[PAYMENT_REPO] Registro creado exitosamente - Payment ID: {payment.id}"
            )

            return payment

        except Exception as e:
            logger.error(
                f"[PAYMENT_REPO] Error al crear registro - "
                f"User ID: {user_id}, "
                f"Reference: {reference}, "
                f"Error: {str(e)}",
                exc_info=True,
            )
            raise

    def get_by_id(self, payment_id: int):
        logger.debug(f"[PAYMENT_REPO] Buscando pago por ID: {payment_id}")
        return Payment.objects.filter(id=payment_id).first()

    def get_by_transaction_id(self, transaction_id: str):
        logger.debug(
            f"[PAYMENT_REPO] Buscando pago por Transaction ID: {transaction_id}"
        )
        return Payment.objects.filter(wompi_transaction_id=transaction_id).first()

    def update_status(self, payment_id: int, status: str):
        try:
            logger.info(
                f"[PAYMENT_REPO] Actualizando status - "
                f"Payment ID: {payment_id}, "
                f"New Status: {status}"
            )

            payment = self.get_by_id(payment_id)
            if payment:
                old_status = payment.status
                payment.status = status
                payment.save()

                logger.info(
                    f"[PAYMENT_REPO] Status actualizado - "
                    f"Payment ID: {payment_id}, "
                    f"Old: {old_status}, "
                    f"New: {status}"
                )
            else:
                logger.warning(
                    f"[PAYMENT_REPO] Pago no encontrado - Payment ID: {payment_id}"
                )

            return payment

        except Exception as e:
            logger.error(
                f"[PAYMENT_REPO] Error al actualizar status - "
                f"Payment ID: {payment_id}, "
                f"Error: {str(e)}",
                exc_info=True,
            )
            raise
