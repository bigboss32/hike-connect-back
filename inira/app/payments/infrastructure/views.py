# inira/app/payments/infrastructure/api/payments_api.py

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime

from inira.app.payments.infrastructure.docs.get_payment_status_docs import (
    get_payment_status_docs,
)
from inira.app.payments.infrastructure.docs.post_payment_docs import post_payment_docs
from inira.app.payments.infrastructure.input.payment_serializer import (
    ProcessPaymentInputSerializer,
)
from inira.app.payments.infrastructure.out.payment_output_serializer import (
    PaymentOutputSerializer,
    PaymentStatusOutputSerializer,
)
from inira.app.shared.container import container

logger = logging.getLogger(__name__)


class PaymentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @post_payment_docs
    def post(self, request):
        """Procesar pago PSE con Wompi para reserva de ruta"""

        input_serializer = ProcessPaymentInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            use_case = container.payments().process_wompi_payment()

            result = use_case.execute(
                {
                    **input_serializer.validated_data,
                    "user_id": request.user.id,
                    "user_email": request.user.email,
                    "timestamp": int(datetime.now().timestamp()),
                }
            )

            output_serializer = PaymentOutputSerializer(data=result)
            output_serializer.is_valid(raise_exception=True)

            return Response(
                output_serializer.validated_data, status=status.HTTP_201_CREATED
            )

        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(
                f"[PAYMENTS_API] Error inesperado - "
                f"User ID: {request.user.id}, "
                f"Error: {str(e)}, "
                f"Type: {type(e).__name__}",
                exc_info=True,
            )
            return Response(
                {"detail": "Error procesando el pago"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PaymentStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @get_payment_status_docs
    def get(self, request, payment_id):
        """Obtener el estado actual de un pago"""

        try:
            use_case = container.payments().check_payment_status()

            result = use_case.execute(
                payment_id=payment_id,
                user_id=request.user.id,
            )

            output_serializer = PaymentStatusOutputSerializer(data=result)
            output_serializer.is_valid(raise_exception=True)

            return Response(output_serializer.validated_data, status=status.HTTP_200_OK)

        except PermissionError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_403_FORBIDDEN,
            )
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(
                f"[PAYMENT_STATUS_API] Error inesperado - "
                f"Payment ID: {payment_id}, "
                f"User ID: {request.user.id}, "
                f"Error: {str(e)}",
                exc_info=True,
            )
            return Response(
                {"detail": "Error al consultar estado del pago"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
