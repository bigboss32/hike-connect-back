# inira/app/payments/admin.py

from django.contrib import admin

from inira.app.payments.infrastructure.models import *


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "wompi_reference",
        "user",
        "ruta",
        "amount",
        "status",
        "booking_date",
        "total_participants",
        "created_at",
    ]
    list_filter = ["status", "payment_method", "payment_type", "created_at"]
    search_fields = [
        "wompi_reference",
        "wompi_transaction_id",
        "user__email",
        "payer_full_name",
    ]
    readonly_fields = [
        "id",
        "wompi_transaction_id",
        "wompi_reference",
        "created_at",
        "updated_at",
        "completed_at",
    ]


@admin.register(PaymentParticipant)
class PaymentParticipantAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "payment",
        "is_titular",
        "order",
        "phone",
        "created_at",
    ]
    list_filter = ["is_titular", "created_at"]
    search_fields = ["full_name", "phone", "payment__wompi_reference"]


@admin.register(PaymentWebhookLog)
class PaymentWebhookLogAdmin(admin.ModelAdmin):
    list_display = [
        "transaction_id",
        "event_type",
        "status",
        "processed",
        "created_at",
    ]
    list_filter = ["processed", "event_type", "status", "created_at"]
    search_fields = ["transaction_id"]
    readonly_fields = ["raw_payload"]
