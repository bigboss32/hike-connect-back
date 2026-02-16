# inira/app/payments/infrastructure/api/payments_api.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime

from inira.app.payments.infrastructure.docs.get_payment_status_docs import (
    get_payment_status_docs,
)
from inira.app.payments.infrastructure.input.payment_serializer import (
    ProcessPaymentInputSerializer,
)
from inira.app.payments.infrastructure.out.payment_output_serializer import (
    PaymentOutputSerializer,
)
from inira.app.shared.container import container

from inira.app.payments.infrastructure.docs.post_payment_docs import post_payment_docs


class PaymentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @post_payment_docs
    def post(self, request):
        """Procesar pago PSE con Wompi"""

        # Validar datos de entrada
        input_serializer = ProcessPaymentInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        try:
            use_case = container.payments().process_wompi_payment()

            # Preparar datos para el use case
            payment_data = {
                **validated_data,
                "user_id": request.user.id,
                "user_email": request.user.email,
                "user_phone": validated_data.get("phone_number")
                or getattr(request.user, "phone", ""),
                "user_full_name": validated_data.get("full_name")
                or request.user.get_full_name()
                or request.user.username,
                "timestamp": int(datetime.now().timestamp()),
            }

            result = use_case.execute(payment_data)

            # Serializar la salida
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
            # TODO: Log the error here
            return Response(
                {"detail": "Error procesando el pago"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# inira/app/payments/infrastructure/api/payment_status_api.py


class PaymentStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @get_payment_status_docs
    def get(self, request, payment_id):
        """Obtener el estado actual de un pago"""

        try:
            use_case = container.payments().check_payment_status()
            result = use_case.execute(payment_id=payment_id)
            payment = container.payments().payment_repository().get_by_id(payment_id)
            if payment.user_id != request.user.id:
                return Response(
                    {"detail": "No tiene permisos para acceder a este pago"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            return Response(result, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"detail": "Error al consultar estado del pago"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
