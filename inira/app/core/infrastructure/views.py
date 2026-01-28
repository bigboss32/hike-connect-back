import requests
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class TestEmailAPIView(APIView):

    def post(self, request):
        to_email = request.data.get("email")

        if not to_email:
            return Response(
                {"detail": "email es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            response = requests.post(
                f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages",
                auth=("api", settings.MAILGUN_API_KEY),
                data={
                    "from": settings.DEFAULT_FROM_EMAIL,
                    "to": to_email,
                    "subject": "Prueba desde Django DRF",
                    "text": "Este correo fue enviado desde Django usando Mailgun (sandbox).",
                },
                timeout=10,
            )

            return Response(
                {
                    "mailgun_status": response.status_code,
                    "mailgun_response": response.text,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
