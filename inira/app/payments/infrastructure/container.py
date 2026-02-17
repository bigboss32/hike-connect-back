# inira/app/payments/infrastructure/containers/payments_container.py

from dependency_injector import containers, providers
from inira.app.payments.application.use_cases.process_wompi_payment import (
    ProcessWompiPayment,
)
from inira.app.payments.application.use_cases.check_payment_status import (
    CheckPaymentStatus,
)
from inira.app.payments.domain.services.wompi_services_impl import WompiServiceImpl
from inira.app.payments.infrastructure.repositories.payment_repository_impl import (
    PaymentRepositoryImpl,
)
from inira.app.routes.infrastructure.repositories import RoutesRepositoryImpl


class PaymentsContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias del módulo payments."""

    # Repositories
    payment_repository = providers.Factory(PaymentRepositoryImpl)
    routes_repository = providers.Factory(RoutesRepositoryImpl)  # 👈

    # Services
    wompi_service = providers.Factory(WompiServiceImpl)

    # Use Cases
    process_wompi_payment = providers.Factory(
        ProcessWompiPayment,
        wompi_service=wompi_service,
        payment_repository=payment_repository,
        routes_repository=routes_repository,  # 👈
    )

    check_payment_status = providers.Factory(
        CheckPaymentStatus,
        wompi_service=wompi_service,
        payment_repository=payment_repository,
    )
