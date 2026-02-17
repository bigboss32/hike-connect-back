# inira/app/payments/infrastructure/repositories/payment_repository_impl.py

import logging
from django.db import transaction
from django.utils import timezone

from inira.app.payments.domain.repositories.payment_repository import PaymentRepository
from inira.app.payments.infrastructure.models import Payment, PaymentParticipant

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
        # 🆕 Nuevos campos
        ruta_id: str = None,
        booking_date=None,
        total_participants: int = 1,
        payer_email: str = "",
        payer_phone: str = "",
        payer_full_name: str = "",
        bank_code: str = None,
        user_type: str = None,
        notes: str = "",
        participants: list = None,
    ):
        try:
            logger.info(
                f"[PAYMENT_REPO] Creando registro - "
                f"User ID: {user_id}, "
                f"Transaction ID: {wompi_transaction_id}, "
                f"Reference: {reference}, "
                f"Ruta ID: {ruta_id}, "
                f"Participants: {total_participants}"
            )

            with transaction.atomic():
                # 🔹 Convertir amount_in_cents a COP (dividir por 100)
                amount_cop = amount_in_cents / 100

                # 🔹 Crear el pago principal
                payment = Payment.objects.create(
                    user_id=user_id,
                    ruta_id=str(ruta_id) if ruta_id else None,  # 👈 convertir a str
                    wompi_transaction_id=wompi_transaction_id,
                    wompi_reference=reference,
                    amount=amount_cop,
                    status=status,
                    payment_method=payment_method_type,
                    booking_date=booking_date,
                    total_participants=total_participants,
                    payer_email=payer_email,
                    payer_phone=payer_phone,
                    payer_full_name=payer_full_name,
                    bank_code=bank_code,
                    user_type=user_type,
                    notes=notes or "",
                )

                logger.info(f"[PAYMENT_REPO] Pago creado - Payment ID: {payment.id}")

                # 🆕 Crear los participantes si se proporcionan
                if participants:
                    self._create_participants(payment, participants)

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

    def _create_participants(self, payment: Payment, participants: list):
        """Crea los participantes asociados al pago"""
        participant_objects = []

        for index, participant_data in enumerate(participants, start=1):
            is_titular = index == 1

            participant = PaymentParticipant(
                payment=payment,
                full_name=participant_data["full_name"],
                phone=participant_data["phone"],
                emergency_contact_name=participant_data["emergency_contact_name"],
                emergency_contact_phone=participant_data["emergency_contact_phone"],
                is_titular=is_titular,
                order=index,
            )
            participant_objects.append(participant)

            logger.debug(
                f"[PAYMENT_REPO] Participante preparado - "
                f"Order: {index}, "
                f"Name: {participant_data['full_name']}, "
                f"Titular: {is_titular}"
            )

        # Bulk create para optimizar queries
        PaymentParticipant.objects.bulk_create(participant_objects)

        logger.info(
            f"[PAYMENT_REPO] {len(participant_objects)} participantes creados - "
            f"Payment ID: {payment.id}"
        )

    def get_by_id(self, payment_id: str):
        logger.debug(f"[PAYMENT_REPO] Buscando pago por ID: {payment_id}")
        return (
            Payment.objects.prefetch_related(
                "participants"
            )  # 🆕 Trae los participantes en la misma query
            .filter(id=payment_id)
            .first()
        )

    def get_by_transaction_id(self, transaction_id: str):
        logger.debug(
            f"[PAYMENT_REPO] Buscando pago por Transaction ID: {transaction_id}"
        )
        return (
            Payment.objects.prefetch_related("participants")  # 🆕
            .filter(wompi_transaction_id=transaction_id)
            .first()
        )

    def get_by_reference(self, reference: str):
        logger.debug(f"[PAYMENT_REPO] Buscando pago por Reference: {reference}")
        return (
            Payment.objects.prefetch_related("participants")
            .filter(wompi_reference=reference)
            .first()
        )

    def update_status(self, payment_id: str, status: str):
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

                # 🆕 Si se aprueba, registrar la fecha de completado
                if status == Payment.PaymentStatus.APPROVED:
                    payment.completed_at = timezone.now()
                    payment.save(update_fields=["status", "completed_at", "updated_at"])
                else:
                    payment.save(update_fields=["status", "updated_at"])

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

    def get_user_payments(self, user_id: int):
        """🆕 Obtiene todos los pagos de un usuario"""
        logger.debug(f"[PAYMENT_REPO] Buscando pagos del usuario: {user_id}")
        return (
            Payment.objects.filter(user_id=user_id)
            .prefetch_related("participants")
            .select_related("ruta")
            .order_by("-created_at")
        )

    # inira/app/payments/infrastructure/repositories/payment_repository_impl.py

    def update_status_and_url(
        self,
        payment_id: str,
        status: str,
        redirect_url: str = None,
    ):
        try:
            logger.info(
                f"[PAYMENT_REPO] Actualizando status y URL - "
                f"Payment ID: {payment_id}, "
                f"New Status: {status}, "
                f"Has URL: {bool(redirect_url)}"
            )

            payment = self.get_by_id(payment_id)

            if not payment:
                logger.warning(f"[PAYMENT_REPO] Pago no encontrado - ID: {payment_id}")
                return None

            old_status = payment.status
            fields_to_update = ["status", "updated_at"]

            payment.status = status

            # 🔹 Guardar URL solo si viene y no estaba guardada
            if redirect_url and not payment.wompi_payment_link:
                payment.wompi_payment_link = redirect_url
                fields_to_update.append("wompi_payment_link")

            # 🔹 Si se aprueba, registrar fecha
            if status == Payment.PaymentStatus.APPROVED:
                from django.utils import timezone

                payment.completed_at = timezone.now()
                fields_to_update.append("completed_at")

            payment.save(update_fields=fields_to_update)

            logger.info(
                f"[PAYMENT_REPO] Pago actualizado - "
                f"Payment ID: {payment_id}, "
                f"Status: {old_status} → {status}, "
                f"Fields: {fields_to_update}"
            )

            return payment

        except Exception as e:
            logger.error(
                f"[PAYMENT_REPO] Error al actualizar - "
                f"Payment ID: {payment_id}, "
                f"Error: {str(e)}",
                exc_info=True,
            )
            raise
