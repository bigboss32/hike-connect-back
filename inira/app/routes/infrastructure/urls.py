from django.urls import path
from .views import RutaSenderismoAPIView

urlpatterns = [
    path("rutas/", RutaSenderismoAPIView.as_view(), name="rutas"),
]
