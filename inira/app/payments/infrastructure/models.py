# inira/app/payments/infrastructure/models/payment.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Payment(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pendiente"),
        ("APPROVED", "Aprobado"),
        ("DECLINED", "Rechazado"),
        ("VOIDED", "Anulado"),
        ("ERROR", "Error"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wompi_transaction_id = models.CharField(max_length=255, unique=True)
    amount_in_cents = models.BigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    payment_method_type = models.CharField(max_length=50)
    reference = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payments"
        indexes = [
            models.Index(fields=["wompi_transaction_id"]),
            models.Index(fields=["reference"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"Payment {self.reference} - {self.status}"
