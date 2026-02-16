# inira/app/payments/infrastructure/serializers/payment_output_serializer.py

from rest_framework import serializers


class PaymentOutputSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField()
    transaction_id = serializers.CharField()
    status = serializers.CharField()
    redirect_url = serializers.URLField(allow_null=True)

    class Meta:
        fields = ["payment_id", "transaction_id", "status", "redirect_url"]


class PaymentStatusOutputSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField()
    transaction_id = serializers.CharField()
    status = serializers.CharField()
    amount_in_cents = serializers.IntegerField()
    reference = serializers.CharField()
    redirect_url = serializers.URLField(allow_null=True)
    ticket_id = serializers.CharField(allow_null=True)
    return_code = serializers.CharField(allow_null=True)
    created_at = serializers.DateTimeField(allow_null=True)
    updated_at = serializers.DateTimeField(allow_null=True)
