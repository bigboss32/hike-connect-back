# inira/app/payments/infrastructure/serializers/payment_input_serializer.py

from rest_framework import serializers


class ProcessPaymentInputSerializer(serializers.Serializer):
    amount_in_cents = serializers.IntegerField(
        required=True,
        min_value=1,
        error_messages={
            "required": "El monto es requerido",
            "min_value": "El monto debe ser mayor a 0",
        },
    )

    user_legal_id = serializers.CharField(
        required=True,
        max_length=50,
        error_messages={
            "required": "La cédula es requerida",
            "blank": "La cédula no puede estar vacía",
        },
    )

    user_legal_id_type = serializers.ChoiceField(
        choices=["CC", "CE", "NIT", "PP", "TI"],
        default="CC",
        error_messages={
            "invalid_choice": "Tipo de documento inválido. Opciones: CC, CE, NIT, PP, TI"
        },
    )

    financial_institution_code = serializers.CharField(
        required=True,
        error_messages={
            "required": "El código de la institución financiera es requerido",
            "blank": "El código de la institución financiera no puede estar vacío",
        },
    )

    user_type = serializers.ChoiceField(
        choices=[0, 1],  # 0 = Persona natural, 1 = Persona jurídica
        default=0,
        error_messages={
            "invalid_choice": "Tipo de usuario inválido. 0 = Persona natural, 1 = Persona jurídica"
        },
    )

    phone_number = serializers.CharField(
        required=False, max_length=20, allow_blank=True
    )

    full_name = serializers.CharField(required=False, max_length=255, allow_blank=True)

    reference = serializers.CharField(
        required=False,
        max_length=255,
        allow_blank=True,
        help_text="Referencia del pago (opcional, se genera automáticamente si no se proporciona)",
    )

    def validate_user_legal_id(self, value):
        """Validar que la cédula solo contenga números"""
        if not value.isdigit():
            raise serializers.ValidationError("La cédula debe contener solo números")
        return value

    def validate_financial_institution_code(self, value):
        """Validar que el código de la institución sea válido"""
        if not value.isdigit():
            raise serializers.ValidationError("El código debe ser numérico")
        return value

    def validate_phone_number(self, value):
        """Validar formato de teléfono si se proporciona"""
        if value and not value.replace("+", "").isdigit():
            raise serializers.ValidationError("El teléfono debe contener solo números")
        return value
