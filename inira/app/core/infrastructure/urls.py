from django.urls import path

from .views import CoreAPIView

urlpatterns = [
    path("", CoreAPIView.as_view(), name="CoreAPIView"),
   
]
