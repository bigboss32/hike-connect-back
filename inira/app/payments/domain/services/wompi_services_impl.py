# inira/app/payments/infrastructure/services/wompi_service_impl.py

import hashlib
import requests
import logging
from django.conf import settings
from django.core.cache import cache
from inira.app.payments.domain.services.wompi_services import WompiService

logger = logging.getLogger(__name__)


class WompiServiceImpl(WompiService):
    def __init__(self):
        self.base_url = settings.WOMPI_BASE_URL
        self.private_key = settings.WOMPI_PRIVATE_KEY
        self.public_key = settings.WOMPI_PUBLIC_KEY
        self.integrity_secret = settings.WOMPI_INTEGRITY_SECRET

        # Cache keys
        self.ACCEPTANCE_TOKEN_CACHE_KEY = "wompi_acceptance_token"
        self.PERSONAL_AUTH_TOKEN_CACHE_KEY = "wompi_personal_auth_token"

    def _get_merchant_info(self):
        """Obtiene la información del merchant desde Wompi API"""
        try:
            logger.info("[WOMPI_MERCHANT] Obteniendo información del merchant")

            url = f"{self.base_url}merchants/{self.public_key}"

            logger.debug(f"[WOMPI_MERCHANT] URL: {url}")

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            merchant_data = response.json()

            logger.info("[WOMPI_MERCHANT] Información obtenida exitosamente")
            logger.debug(f"[WOMPI_MERCHANT] Response: {merchant_data}")

            return merchant_data.get("data", {})

        except requests.exceptions.RequestException as e:
            logger.error(
                f"[WOMPI_MERCHANT] Error al obtener información - Error: {str(e)}",
                exc_info=True,
            )
            raise Exception(f"Error al obtener información del merchant: {str(e)}")

    def _get_acceptance_tokens(self):
        """
        Obtiene los tokens de aceptación desde cache o API.
        Retorna: (acceptance_token, accept_personal_auth)
        """
        # Intentar obtener desde cache
        acceptance_token = cache.get(self.ACCEPTANCE_TOKEN_CACHE_KEY)
        personal_auth_token = cache.get(self.PERSONAL_AUTH_TOKEN_CACHE_KEY)

        if acceptance_token and personal_auth_token:
            logger.info("[WOMPI_TOKENS] Tokens obtenidos desde cache")
            return acceptance_token, personal_auth_token

        logger.info(
            "[WOMPI_TOKENS] Tokens no encontrados en cache, obteniendo desde API"
        )
        merchant_info = self._get_merchant_info()
        presigned_acceptance = merchant_info.get("presigned_acceptance", {})
        presigned_personal_data = merchant_info.get("presigned_personal_data_auth", {})
        acceptance_token = presigned_acceptance.get("acceptance_token")
        personal_auth_token = presigned_personal_data.get("acceptance_token")

        if not acceptance_token or not personal_auth_token:
            logger.error(
                "[WOMPI_TOKENS] Tokens no encontrados en la respuesta del merchant"
            )
            raise Exception(
                "No se pudieron obtener los tokens de aceptación desde Wompi"
            )

        logger.info("[WOMPI_TOKENS] Tokens obtenidos y guardados en cache")

        return acceptance_token, personal_auth_token

    def _generate_signature(
        self, reference: str, amount_in_cents: int, currency: str = "COP"
    ) -> str:
        """Genera la firma de integridad para Wompi"""
        cadena = f"{reference}{amount_in_cents}{currency}{self.integrity_secret}"
        signature = hashlib.sha256(cadena.encode("utf-8")).hexdigest()

        logger.debug(
            f"[WOMPI_SIGNATURE] Generada - Reference: {reference}, Amount: {amount_in_cents}"
        )

        return signature

    def create_pse_transaction(
        self,
        amount_in_cents: int,
        reference: str,
        customer_email: str,
        customer_phone: str,
        customer_full_name: str,
        user_legal_id: str,
        user_legal_id_type: str = "CC",
        user_type: int = 0,
        financial_institution_code: str = "1",
        currency: str = "COP",
    ):
        """Crea una transacción PSE en Wompi"""

        logger.info(
            f"[WOMPI_API] Preparando request - "
            f"Reference: {reference}, "
            f"Amount: {amount_in_cents}, "
            f"Email: {customer_email}, "
            f"Bank: {financial_institution_code}"
        )

        # Obtener tokens de aceptación
        acceptance_token, accept_personal_auth = self._get_acceptance_tokens()

        # Generar firma
        signature = self._generate_signature(reference, amount_in_cents, currency)

        # Construir payload
        payload = {
            "acceptance_token": acceptance_token,
            "accept_personal_auth": accept_personal_auth,
            "amount_in_cents": amount_in_cents,
            "currency": currency,
            "reference": reference,
            "customer_email": customer_email,
            "signature": signature,
            "payment_method": {
                "type": "PSE",
                "user_type": user_type,
                "user_legal_id_type": user_legal_id_type,
                "user_legal_id": user_legal_id,
                "financial_institution_code": financial_institution_code,
                "payment_description": f"Pago - {reference}",
            },
            "customer_data": {
                "phone_number": customer_phone,
                "full_name": customer_full_name,
            },
        }

        # Headers
        headers = {
            "Authorization": f"Bearer {self.private_key}",
            "Content-Type": "application/json",
        }

        url = f"{self.base_url}transactions"

        # Realizar request
        try:
            logger.info(f"[WOMPI_API] Enviando request a: {url}")

            response = requests.post(url, json=payload, headers=headers, timeout=30)

            logger.info(
                f"[WOMPI_API] Response recibida - "
                f"Status Code: {response.status_code}, "
                f"Reference: {reference}"
            )

            if settings.DEBUG:
                logger.debug(f"[WOMPI_API] Response body: {response.text}")

            response.raise_for_status()
            response_data = response.json()

            logger.info(
                f"[WOMPI_API] Transacción creada - "
                f"Transaction ID: {response_data.get('data', {}).get('id')}, "
                f"Status: {response_data.get('data', {}).get('status')}"
            )

            return response_data

        except requests.exceptions.Timeout as e:
            logger.error(
                f"[WOMPI_API] Timeout - Reference: {reference}, Error: {str(e)}"
            )
            raise Exception("Timeout al conectar con Wompi")

        except requests.exceptions.HTTPError as e:
            logger.error(
                f"[WOMPI_API] HTTP Error - "
                f"Reference: {reference}, "
                f"Status Code: {response.status_code}, "
                f"Response: {response.text}"
            )
            raise Exception(f"Error en Wompi API: {response.text}")

        except requests.exceptions.RequestException as e:
            logger.error(
                f"[WOMPI_API] Request Error - Reference: {reference}, Error: {str(e)}"
            )
            raise Exception(f"Error de conexión con Wompi: {str(e)}")

        except Exception as e:
            logger.error(
                f"[WOMPI_API] Error inesperado - "
                f"Reference: {reference}, "
                f"Error: {str(e)}",
                exc_info=True,
            )
            raise

    def get_transaction_status(self, transaction_id: str):
        """Obtiene el estado actual de una transacción"""

        logger.info(
            f"[WOMPI_STATUS] Consultando estado - Transaction ID: {transaction_id}"
        )

        url = f"{self.base_url}transactions/{transaction_id}"

        try:
            logger.debug(f"[WOMPI_STATUS] URL: {url}")

            response = requests.get(url, timeout=10)

            logger.info(
                f"[WOMPI_STATUS] Response recibida - "
                f"Status Code: {response.status_code}, "
                f"Transaction ID: {transaction_id}"
            )

            if settings.DEBUG:
                logger.debug(f"[WOMPI_STATUS] Response body: {response.text}")

            response.raise_for_status()
            response_data = response.json()

            status = response_data.get("data", {}).get("status")
            logger.info(
                f"[WOMPI_STATUS] Estado obtenido - "
                f"Transaction ID: {transaction_id}, "
                f"Status: {status}"
            )

            return response_data

        except requests.exceptions.Timeout as e:
            logger.error(
                f"[WOMPI_STATUS] Timeout - Transaction ID: {transaction_id}, Error: {str(e)}"
            )
            raise Exception("Timeout al consultar estado de transacción")

        except requests.exceptions.HTTPError as e:
            logger.error(
                f"[WOMPI_STATUS] HTTP Error - "
                f"Transaction ID: {transaction_id}, "
                f"Status Code: {response.status_code}, "
                f"Response: {response.text}"
            )
            raise Exception(f"Error al consultar transacción: {response.text}")

        except Exception as e:
            logger.error(
                f"[WOMPI_STATUS] Error inesperado - "
                f"Transaction ID: {transaction_id}, "
                f"Error: {str(e)}",
                exc_info=True,
            )
            raise

    def get_financial_institutions(self) -> list:
        """Obtiene la lista de bancos PSE disponibles"""

        url = f"{self.base_url}pse/financial_institutions"

        logger.info("[WOMPI_BANKS] Obteniendo instituciones financieras")

        try:
            response = requests.get(
                url,
                headers={"Authorization": f"Bearer {self.public_key}"},
                timeout=10,
            )

            logger.info(
                f"[WOMPI_BANKS] Response recibida - Status Code: {response.status_code}"
            )

            response.raise_for_status()
            response_data = response.json()

            institutions = response_data.get("data", [])

            logger.info(
                f"[WOMPI_BANKS] Instituciones obtenidas - Total: {len(institutions)}"
            )

            return institutions

        except requests.exceptions.Timeout as e:
            logger.error(f"[WOMPI_BANKS] Timeout - Error: {str(e)}")
            raise Exception("Timeout al obtener instituciones financieras")

        except requests.exceptions.HTTPError as e:
            logger.error(
                f"[WOMPI_BANKS] HTTP Error - "
                f"Status Code: {response.status_code}, "
                f"Response: {response.text}"
            )
            raise Exception(f"Error en Wompi API: {response.text}")

        except requests.exceptions.RequestException as e:
            logger.error(f"[WOMPI_BANKS] Request Error - Error: {str(e)}")
            raise Exception(f"Error de conexión con Wompi: {str(e)}")

        except Exception as e:
            logger.error(
                f"[WOMPI_BANKS] Error inesperado - Error: {str(e)}", exc_info=True
            )
            raise
