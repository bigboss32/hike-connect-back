from django.urls import path

from .views import LoginAPIView,RegisterAPIView

urlpatterns = [
    path("login", LoginAPIView.as_view(), name="inico de sesion"),
    path("register", RegisterAPIView.as_view(), name="registro de usuarios"),

   
]
