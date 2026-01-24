# inira/app/communities/infrastructure/api/urls.py

from django.urls import path
from .views import (
    ComunidadAPIView,
    ComunidadMemberAPIView,
    ComunidadCanalAPIView,
    ComunidadPostAPIView,
)

urlpatterns = [
    # Comunidades
    path("comunidad/", ComunidadAPIView.as_view(), name="ComunidadAPIView"),
    
    # Miembros
    path("comunidad-member/", ComunidadMemberAPIView.as_view(), name="ComunidadMemberAPIView"),
    
    # Canales
    path("comunidad-canal/", ComunidadCanalAPIView.as_view(), name="ComunidadCanalAPIView"),
    
    # Posts
    path("comunidad-post/", ComunidadPostAPIView.as_view(), name="ComunidadPostAPIView"),
]