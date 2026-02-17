# inira/app/payments/application/use_cases/process_wompi_payment.py

import logging
from inira.app.payments.domain.services.wompi_services import WompiService
from inira.app.payments.domain.repositories.payment_repository import PaymentRepository
from inira.app.routes.domain.entities import RouteEntity
from inira.app.routes.domain.repositories import RoutesRepository
from inira.app.routes.infrastructure.models import RutaAvailability

logger = logging.getLogger(__name__)


class ProcessWompiPayment:
    def __init__(
        self,
        wompi_service: WompiService,
        payment_repository: PaymentRepository,
        routes_repository: RoutesRepository,  # 🆕
    ):
        self.wompi_service = wompi_service
        self.payment_repository = payment_repository
        self.routes_repository = routes_repository

    def execute(self, payment_data: dict):

        user_id = payment_data["user_id"]
        ruta_id = payment_data["ruta_id"]
        booking_date = payment_data["booking_date"]
        participants = payment_data.get("participants", [])
        total_participants = len(participants)

        logger.info(
            f"[INICIO] Procesando pago - "
            f"User ID: {user_id}, "
            f"Ruta ID: {ruta_id}, "
            f"Participants: {total_participants}"
        )

        try:
            # 1. Validar que la ruta exista y esté activa
            ruta: RouteEntity = self.routes_repository.find_by_id(ruta_id)

            if not ruta.is_active:
                raise ValueError("Esta ruta no está disponible actualmente")

            # 2. Validar límites de participantes
            ruta.validate_booking_capacity(total_participants)

            # 3. Validar disponibilidad por fecha
            availability: RutaAvailability = (
                self.routes_repository.get_availability_for_date(ruta_id, booking_date)
            )

            if not availability.has_available_slots:
                raise ValueError("No hay cupos disponibles para esta fecha")

            if availability.available_slots < total_participants:
                raise ValueError(
                    f"Solo quedan {availability.available_slots} cupos disponibles"
                )

            # 4. Calcular monto en centavos desde el precio de la ruta
            amount_in_cents = int(ruta.base_price * total_participants * 100)

            logger.info(
                f"[VALIDACIÓN] Ruta válida - "
                f"Price: {ruta.base_price}, "
                f"Participants: {total_participants}, "
                f"Total cents: {amount_in_cents}"
            )

            # 5. Generar referencia
            reference = (
                payment_data.get("reference")
                or f"PAY_USER_{user_id}_{payment_data.get('timestamp', '')}"
            )

            logger.info(f"[REFERENCIA] Generada: {reference}")

            # 6. Crear la transacción en Wompi
            wompi_response = self.wompi_service.create_pse_transaction(
                amount_in_cents=amount_in_cents,
                reference=reference,
                customer_email=payment_data["user_email"],
                customer_phone=participants[0]["phone"],
                customer_full_name=participants[0]["full_name"],
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
                f"[WOMPI] Transacción creada - "
                f"Transaction ID: {transaction_id}, "
                f"Status: {transaction_status}"
            )

            # 7. Guardar el pago con participantes
            payment = self.payment_repository.create(
                user_id=user_id,
                wompi_transaction_id=transaction_id,
                amount_in_cents=amount_in_cents,
                status=transaction_status,
                payment_method_type="PSE",
                reference=reference,
                ruta_id=ruta_id,
                booking_date=booking_date,
                total_participants=total_participants,
                payer_email=payment_data["user_email"],
                payer_phone=participants[0]["phone"],
                payer_full_name=participants[0]["full_name"],
                bank_code=payment_data.get("financial_institution_code"),
                user_type=str(payment_data.get("user_type", "0")),
                participants=participants,
            )

            logger.info(f"[DB] Pago guardado - Payment ID: {payment.id}")

            return {
                "payment_id": str(payment.id),
                "transaction_id": transaction_id,
                "status": transaction_status,
                "redirect_url": redirect_url,
                "ruta_id": str(ruta_id),
                "booking_date": str(booking_date),
                "total_participants": total_participants,
                "amount": str(payment.amount),
            }

        except ValueError:
            raise

        except KeyError as e:
            logger.error(f"[ERROR] Campo faltante: {str(e)} - User ID: {user_id}")
            raise ValueError(f"Campo requerido faltante: {str(e)}")

        except Exception as e:
            logger.error(
                f"[ERROR] Error inesperado - User ID: {user_id}, Error: {str(e)}",
                exc_info=True,
            )
            raise
