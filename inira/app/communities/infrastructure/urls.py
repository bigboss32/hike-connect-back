from django.urls import path
from .views import EventoInscripcionAPIView,EventoAPIView

urlpatterns = [
    path("evento-inscripcion/", EventoInscripcionAPIView.as_view(), name="EventoInscripcionAPIView"),
    path("evento/", EventoAPIView.as_view(), name="Evento"),
]
