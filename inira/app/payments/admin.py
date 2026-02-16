from django.contrib import admin

from inira.app.payments.infrastructure.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "reference",
        "user",
        "amount_in_cents",
        "status",
        "payment_method_type",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method_type",
        "created_at",
    )

    search_fields = (
        "reference",
        "wompi_transaction_id",
        "user__email",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "wompi_transaction_id",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Información General",
            {
                "fields": (
                    "user",
                    "reference",
                    "wompi_transaction_id",
                    "amount_in_cents",
                    "status",
                    "payment_method_type",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
