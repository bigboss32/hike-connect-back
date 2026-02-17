import json
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

logger = logging.getLogger(__name__)


class WebHookAPIView(APIView):
    permission_classes = [AllowAny]  # importante para que Wompi pueda llamar

    def post(self, request):

        print("🔥 WEBHOOK RECIBIDO 🔥")
        print(json.dumps(request.data, indent=4))

        logger.info("Webhook recibido de Wompi")
        logger.info(json.dumps(request.data, indent=4))

        return Response(
            {"message": "Webhook recibido correctamente"},
            status=status.HTTP_200_OK,
        )
