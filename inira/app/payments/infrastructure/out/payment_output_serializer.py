# inira/app/payments/infrastructure/out/payment_output_serializer.py

from rest_framework import serializers


class PaymentOutputSerializer(serializers.Serializer):
    payment_id = serializers.CharField()
    transaction_id = serializers.CharField()
    status = serializers.CharField()
    redirect_url = serializers.URLField(allow_null=True)
    # 🆕
    ruta_id = serializers.CharField(allow_null=True)
    booking_date = serializers.CharField(allow_null=True)
    total_participants = serializers.IntegerField()
    amount = serializers.CharField()


class PaymentStatusOutputSerializer(serializers.Serializer):
    payment_id = serializers.CharField()  # 🔹 CharField, ahora es UUID
    transaction_id = serializers.CharField()
    status = serializers.CharField()
    amount = serializers.CharField()  # 🔹 Cambiado de amount_in_cents a amount en COP
    reference = serializers.CharField()
    redirect_url = serializers.URLField(allow_null=True)
    ticket_id = serializers.CharField(allow_null=True)
    return_code = serializers.CharField(allow_null=True)
    # 🆕
    ruta_id = serializers.CharField(allow_null=True)
    booking_date = serializers.CharField(allow_null=True)
    total_participants = serializers.IntegerField(allow_null=True)
    created_at = serializers.DateTimeField(allow_null=True)
    updated_at = serializers.DateTimeField(allow_null=True)
