from django.urls import path
from .views import PaymentStatusAPIView, PaymentsAPIView

urlpatterns = [
    path("payments/", PaymentsAPIView.as_view(), name="PaymentsAPIView"),
    path(
        "payments/<str:payment_id>/status/",
        PaymentStatusAPIView.as_view(),
        name="payment-status",
    ),
]
