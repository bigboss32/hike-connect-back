from django.urls import path

from .views import TestEmailAPIView

urlpatterns = [
    path("", TestEmailAPIView.as_view(), name="CoreAPIView"),
   
]
