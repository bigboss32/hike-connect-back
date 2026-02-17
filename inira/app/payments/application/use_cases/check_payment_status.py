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

    def execute(self, payment_id: str, user_id: int):
        """
        Verifica el estado de un pago en Wompi y actualiza la base de datos.
        Valida que el pago pertenezca al usuario autenticado.
        """

        logger.info(
            f"[CHECK_STATUS] Consultando pago - "
            f"Payment ID: {payment_id}, "
            f"User ID: {user_id}"
        )

        # 1. Buscar el pago
        payment: Payment = self.payment_repository.get_by_id(payment_id)

        if not payment:
            logger.warning(
                f"[CHECK_STATUS] Pago no encontrado - Payment ID: {payment_id}"
            )
            raise ValueError("Pago no encontrado")

        # 2. Validar que el pago pertenece al usuario
        if str(payment.user_id) != str(user_id):
            logger.warning(
                f"[CHECK_STATUS] Acceso denegado - "
                f"Payment ID: {payment_id}, "
                f"Owner: {payment.user_id}, "
                f"Requester: {user_id}"
            )
            raise PermissionError("No tiene permisos para acceder a este pago")

        logger.info(
            f"[CHECK_STATUS] Pago encontrado - "
            f"Payment ID: {payment.id}, "
            f"Transaction ID: {payment.wompi_transaction_id}, "
            f"Current Status: {payment.status}"
        )

        # 3. Consultar estado en Wompi
        wompi_response = self.wompi_service.get_transaction_status(
            payment.wompi_transaction_id
        )

        wompi_data = wompi_response.get("data", {})
        new_status = wompi_data.get("status")

        # 4. Extraer URL de Wompi
        payment_method = wompi_data.get("payment_method", {})
        extra = payment_method.get("extra", {})
        redirect_url = extra.get("async_payment_url")

        # 5. Determinar qué cambió
        status_changed = new_status and new_status != payment.status
        url_is_new = redirect_url and not payment.wompi_payment_link

        # 6. Actualizar en DB si hay cambios
        if status_changed or url_is_new:
            logger.info(
                f"[CHECK_STATUS] Actualizando pago - "
                f"Payment ID: {payment.id}, "
                f"Status changed: {status_changed} ({payment.status} → {new_status}), "
                f"URL nueva: {url_is_new}"
            )

            self.payment_repository.update_status_and_url(
                payment_id=payment.id,
                status=new_status if status_changed else payment.status,
                redirect_url=redirect_url,
            )

            if status_changed:
                payment.status = new_status

            if url_is_new:
                payment.wompi_payment_link = redirect_url

        else:
            logger.info(
                f"[CHECK_STATUS] Sin cambios - "
                f"Payment ID: {payment.id}, "
                f"Status: {payment.status}"
            )

        return {
            "payment_id": str(payment.id),
            "transaction_id": payment.wompi_transaction_id,
            "status": payment.status,
            "amount": str(payment.amount),
            "reference": payment.wompi_reference,
            # 🔹 Usa la nueva URL si vino, si no usa la guardada en DB
            "redirect_url": redirect_url or payment.wompi_payment_link,
            "ticket_id": extra.get("ticket_id"),
            "return_code": extra.get("return_code"),
            "ruta_id": str(payment.ruta_id) if payment.ruta_id else None,
            "booking_date": str(payment.booking_date) if payment.booking_date else None,
            "total_participants": payment.total_participants,
            "created_at": (
                payment.created_at.isoformat() if payment.created_at else None
            ),
            "updated_at": (
                payment.updated_at.isoformat() if payment.updated_at else None
            ),
        }
