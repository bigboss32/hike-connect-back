# inira/app/payments/domain/models/payment.py

import uuid
from django.contrib.gis.db import models
from django.conf import settings
from decimal import Decimal
from django.utils import timezone

from inira.app.routes.infrastructure.models import RutaSenderismo


class Payment(models.Model):
    """
    Modelo principal de pagos.
    Representa un pago realizado por un usuario (titular) que puede incluir múltiples participantes.
    """

    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        APPROVED = "APPROVED", "Aprobado"
        DECLINED = "DECLINED", "Rechazado"
        ERROR = "ERROR", "Error"
        VOIDED = "VOIDED", "Anulado"

    class PaymentMethod(models.TextChoices):
        PSE = "PSE", "PSE"
        CARD = "CARD", "Tarjeta"
        NEQUI = "NEQUI", "Nequi"
        BANCOLOMBIA = "BANCOLOMBIA", "Bancolombia"

    class PaymentType(models.TextChoices):
        BOOKING = "BOOKING", "Reserva de Ruta"
        SUBSCRIPTION = "SUBSCRIPTION", "Suscripción"
        AGROTURISMO = "AGROTURISMO", "Agroturismo"

    # Identificador único
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relaciones - Usuario que PAGA (debe estar logueado)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="payments",
        help_text="Usuario que realiza el pago (titular de la reserva)",
    )

    ruta = models.ForeignKey(
        "routes.RutaSenderismo",
        on_delete=models.PROTECT,
        related_name="payments",
        null=True,
        blank=True,
        help_text="Ruta asociada al pago",
    )

    # Información del pago
    payment_type = models.CharField(
        max_length=20, choices=PaymentType.choices, default=PaymentType.BOOKING
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,  # 👈 AGREGADO
        blank=True,  # 👈 AGREGADO
        help_text="Monto total en COP",
    )

    currency = models.CharField(max_length=3, default="COP")

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        db_index=True,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        null=True,  # 👈 AGREGADO
        blank=True,  # 👈 AGREGADO
    )

    # Wompi específico
    wompi_transaction_id = models.CharField(
        max_length=100, unique=True, null=True, blank=True, db_index=True
    )

    wompi_reference = models.CharField(
        max_length=100,
        unique=True,
        null=True,  # 👈 AGREGADO por si acaso
        blank=True,  # 👈 AGREGADO por si acaso
        db_index=True,
    )

    wompi_payment_link = models.URLField(max_length=500, null=True, blank=True)

    wompi_checkout_url = models.URLField(
        max_length=500, null=True, blank=True, help_text="URL de checkout de Wompi"
    )

    # Información del pagador (usuario titular)
    payer_email = models.EmailField(
        null=True,  # 👈 AGREGADO
        blank=True,  # 👈 AGREGADO
    )

    payer_phone = models.CharField(
        max_length=20,
        null=True,  # 👈 AGREGADO
        blank=True,  # 👈 AGREGADO
    )

    payer_full_name = models.CharField(
        max_length=200,
        null=True,  # 👈 AGREGADO
        blank=True,  # 👈 AGREGADO
    )

    # Información bancaria (PSE)
    bank_name = models.CharField(max_length=100, null=True, blank=True)

    bank_code = models.CharField(max_length=50, null=True, blank=True)

    user_type = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="0: Persona Natural, 1: Persona Jurídica",
    )

    # Detalles de la reserva
    booking_date = models.DateField(
        null=True, blank=True, help_text="Fecha de la excursión", db_index=True
    )

    total_participants = models.PositiveIntegerField(
        default=1,
        null=True,  # 👈 AGREGADO
        blank=True,  # 👈 AGREGADO
        help_text="Número total de participantes (incluyendo titular)",
    )

    # Notas y metadata
    notes = models.TextField(blank=True, help_text="Notas adicionales de la reserva")

    description = models.TextField(blank=True, help_text="Descripción del pago")

    metadata = models.JSONField(
        default=dict, blank=True, help_text="Datos adicionales del pago en formato JSON"
    )

    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(
        null=True, blank=True, help_text="Fecha y hora de aprobación del pago"
    )

    class Meta:
        db_table = "payments"
        ordering = ["-created_at"]
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["ruta", "status"]),
            models.Index(fields=["wompi_transaction_id"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["booking_date"]),
            models.Index(fields=["status", "created_at"]),
        ]

    def __str__(self):
        ruta_info = f" - {self.ruta.title}" if self.ruta else ""
        ref = self.wompi_reference or "SIN-REF"
        return f"Payment {ref}{ruta_info} - {self.status}"

    @property
    def is_successful(self):
        """Verifica si el pago fue exitoso"""
        return self.status == self.PaymentStatus.APPROVED

    @property
    def is_pending(self):
        """Verifica si el pago está pendiente"""
        return self.status == self.PaymentStatus.PENDING

    @property
    def can_be_cancelled(self):
        """Verifica si el pago puede ser cancelado"""
        return self.status in [self.PaymentStatus.PENDING, self.PaymentStatus.APPROVED]

    def mark_as_approved(self):
        """Marca el pago como aprobado"""
        self.status = self.PaymentStatus.APPROVED
        self.completed_at = timezone.now()
        self.save(update_fields=["status", "completed_at", "updated_at"])

    def mark_as_declined(self):
        """Marca el pago como rechazado"""
        self.status = self.PaymentStatus.DECLINED
        self.save(update_fields=["status", "updated_at"])

    def mark_as_error(self):
        """Marca el pago como error"""
        self.status = self.PaymentStatus.ERROR
        self.save(update_fields=["status", "updated_at"])


class PaymentParticipant(models.Model):
    """
    Participantes de una reserva.
    Pueden NO estar registrados en la app.
    El primer participante (order=1) siempre es el titular (quien paga).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="participants"
    )

    # Usuario registrado (opcional - solo si el participante tiene cuenta)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="participant_bookings",
        null=True,
        blank=True,
        help_text="Usuario si está registrado en la app",
    )

    # Datos del participante (siempre requeridos)
    full_name = models.CharField(
        max_length=200, help_text="Nombre completo del participante"
    )

    phone = models.CharField(max_length=20, help_text="Teléfono del participante")

    email = models.EmailField(
        null=True, blank=True, help_text="Email del participante (opcional)"
    )

    # Contacto de emergencia
    emergency_contact_name = models.CharField(
        max_length=200, help_text="Nombre del contacto de emergencia"
    )

    emergency_contact_phone = models.CharField(
        max_length=20, help_text="Teléfono del contacto de emergencia"
    )

    # Control
    is_titular = models.BooleanField(
        default=False, help_text="Si es el titular de la reserva (quien paga)"
    )

    order = models.PositiveSmallIntegerField(
        default=1, help_text="Orden del participante en la lista (1 = titular)"
    )

    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payment_participants"
        ordering = ["order"]
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"
        indexes = [
            models.Index(fields=["payment", "order"]),
            models.Index(fields=["payment", "is_titular"]),
        ]
        unique_together = [["payment", "order"]]

    def __str__(self):
        titular = " (Titular)" if self.is_titular else ""
        ref = self.payment.wompi_reference or "SIN-REF"
        return f"{self.full_name}{titular} - {ref}"

    def save(self, *args, **kwargs):
        # El participante con order=1 siempre es el titular
        if self.order == 1:
            self.is_titular = True
        super().save(*args, **kwargs)


class PaymentWebhookLog(models.Model):
    """
    Log de webhooks recibidos de Wompi.
    Útil para debugging y auditoría.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        related_name="webhook_logs",
        null=True,
        blank=True,
    )

    event_type = models.CharField(
        max_length=100, help_text="Tipo de evento (transaction.updated, etc.)"
    )

    transaction_id = models.CharField(max_length=100, db_index=True)

    status = models.CharField(max_length=50, help_text="Estado recibido en el webhook")

    raw_payload = models.JSONField(help_text="Payload completo del webhook")

    processed = models.BooleanField(
        default=False, help_text="Si el webhook fue procesado exitosamente"
    )

    error_message = models.TextField(
        blank=True, help_text="Mensaje de error si hubo problemas al procesar"
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "payment_webhook_logs"
        ordering = ["-created_at"]
        verbose_name = "Webhook Log"
        verbose_name_plural = "Webhook Logs"
        indexes = [
            models.Index(fields=["transaction_id", "created_at"]),
            models.Index(fields=["processed", "created_at"]),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.transaction_id} - {self.created_at}"
