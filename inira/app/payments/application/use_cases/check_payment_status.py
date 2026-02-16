# inira/app/payments/application/use_cases/check_payment_status.py

import logging
from inira.app.payments.domain.services.wompi_services import WompiService
from inira.app.payments.domain.repositories.payment_repository import PaymentRepository
from inira.app.payments.infrastructure.models import Payment

logger = logging.getLogger(__name__)


class CheckPaymentStatus:
    def __init__(
        self,
        wompi_service: WompiService,
        payment_repository: PaymentRepository,
    ):
        self.wompi_service = wompi_service
        self.payment_repository = payment_repository

    def execute(self, payment_id: int = None, transaction_id: str = None):
        """
        Verifica el estado de un pago en Wompi y actualiza la base de datos.

        Puede recibir payment_id (ID interno) o transaction_id (ID de Wompi)
        """

        if not payment_id and not transaction_id:
            raise ValueError("Debe proporcionar payment_id o transaction_id")

        # Obtener el pago de la base de datos
        if payment_id:
            logger.info(f"[CHECK_STATUS] Buscando pago por Payment ID: {payment_id}")
            payment: Payment = self.payment_repository.get_by_id(payment_id)
        else:
            logger.info(
                f"[CHECK_STATUS] Buscando pago por Transaction ID: {transaction_id}"
            )
            payment = self.payment_repository.get_by_transaction_id(transaction_id)

        if not payment:
            logger.warning(f"[CHECK_STATUS] Pago no encontrado")
            raise ValueError("Pago no encontrado")

        logger.info(
            f"[CHECK_STATUS] Pago encontrado - "
            f"Payment ID: {payment.id}, "
            f"Transaction ID: {payment.wompi_transaction_id}, "
            f"Current Status: {payment.status}"
        )

        # Consultar estado en Wompi
        wompi_response = self.wompi_service.get_transaction_status(
            payment.wompi_transaction_id
        )

        wompi_data = wompi_response.get("data", {})
        new_status = wompi_data.get("status")

        # Actualizar estado si cambió
        if new_status and new_status != payment.status:
            logger.info(
                f"[CHECK_STATUS] Actualizando estado - "
                f"Payment ID: {payment.id}, "
                f"Old Status: {payment.status}, "
                f"New Status: {new_status}"
            )

            self.payment_repository.update_status(payment.id, new_status)
            payment.status = new_status
        else:
            logger.info(
                f"[CHECK_STATUS] Estado sin cambios - "
                f"Payment ID: {payment.id}, "
                f"Status: {payment.status}"
            )

        # Extraer información relevante
        payment_method = wompi_data.get("payment_method", {})
        extra = payment_method.get("extra", {})

        return {
            "payment_id": payment.id,
            "transaction_id": payment.wompi_transaction_id,
            "status": payment.status,
            "amount_in_cents": payment.amount_in_cents,
            "reference": payment.reference,
            "redirect_url": extra.get("async_payment_url"),
            "ticket_id": extra.get("ticket_id"),
            "return_code": extra.get("return_code"),
            "created_at": (
                payment.created_at.isoformat() if payment.created_at else None
            ),
            "updated_at": (
                payment.updated_at.isoformat() if payment.updated_at else None
            ),
        }
