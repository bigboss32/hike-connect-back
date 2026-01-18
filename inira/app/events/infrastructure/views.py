# inira/app/events/infrastructure/api/event_registration_api.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError

from inira.app.shared.container import container
from inira.app.events.infrastructure.out.event_output_serializer import (
    EventOutputSerializer
)
from inira.app.events.infrastructure.docs.get_events_docs import get_events_docs
from inira.app.events.infrastructure.docs.post_event_registration_docs import  post_event_registration_docs

class EventoInscripcionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @post_event_registration_docs
    def post(self, request):
        event_id = request.data.get("event_id")

        if not event_id:
            return Response(
                {"detail": "event_id es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        use_case = container.events().register_user_to_event()

        use_case.execute(
            event_id=event_id,
            user_id=request.user.id,
        )

        return Response(
            {"detail": "Inscripción exitosa"},
            status=status.HTTP_201_CREATED,
        )


class EventoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @get_events_docs
    def get(self, request, *args, **kwargs):
        """
        Query params:
        - id: UUID (opcional)
        - page: int (opcional, default=1)
        - page_size: int (opcional, default=10)
        """

        event_id = request.query_params.get("id")
        page = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 10)
        try:
            page = int(page)
            page_size = int(page_size)
            if page <= 0 or page_size <= 0:
                raise ValueError
        except ValueError:
            raise ValidationError(
                {"detail": "page y page_size deben ser enteros positivos"}
            )

        use_case = container.events().get_events()

        if event_id:
            event = use_case.execute(id=event_id)
            serializer = EventOutputSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)

        result = use_case.execute(
            page=page,
            page_size=page_size,
        )

        events = result["results"]
        total = result["count"]

        serializer = EventOutputSerializer(events, many=True)

        return Response(
            {
                "count": total,
                "page": page,
                "page_size": page_size,
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )