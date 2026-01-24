from django.urls import path
from .views import RutaSenderismoAPIView,RutaRatingAPIView,RutaBannerAPIView

urlpatterns = [
    path("rutas/", RutaSenderismoAPIView.as_view(), name="rutas"),
    path("rate-routes/", RutaRatingAPIView.as_view(), name="rutas"),
    path("ruta-banner/", RutaBannerAPIView.as_view(), name="rutas"),
]
