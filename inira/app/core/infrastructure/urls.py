from django.urls import path

from .views import WebHookAPIView

urlpatterns = [
    path("webhooks", WebHookAPIView.as_view(), name="WebHookAPIView"),
]
