from django.urls import path
from .views import RutaSenderismoAPIView,RutaRatingAPIView

urlpatterns = [
    path("rutas/", RutaSenderismoAPIView.as_view(), name="rutas"),
    path("rate-routes/", RutaRatingAPIView.as_view(), name="rutas"),
]
