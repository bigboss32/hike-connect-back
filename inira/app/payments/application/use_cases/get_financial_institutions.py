# inira/app/payments/application/use_cases/get_financial_institutions.py

import logging
from inira.app.payments.domain.services.wompi_services import WompiService

logger = logging.getLogger(__name__)


class GetFinancialInstitutions:
    def __init__(self, wompi_service: WompiService):
        self.wompi_service = wompi_service

    def execute(self) -> list:
        logger.info("[INICIO] Obteniendo instituciones financieras PSE")

        try:
            institutions = self.wompi_service.get_financial_institutions()

            logger.info(f"[FIN] Instituciones obtenidas - Total: {len(institutions)}")

            return institutions

        except Exception as e:
            logger.error(
                f"[ERROR] Error obteniendo instituciones - Error: {str(e)}",
                exc_info=True,
            )
            raise
