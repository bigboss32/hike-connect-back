from django.urls import path

from .views import LoginAPIView,RegisterAPIView,LogoutAPIView,ProfileAPIView

urlpatterns = [
    path("login", LoginAPIView.as_view(), name="inico de sesion"),
    path("register", RegisterAPIView.as_view(), name="registro de usuarios"),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('profile/', ProfileAPIView.as_view(), name='profile'), 

   
]
