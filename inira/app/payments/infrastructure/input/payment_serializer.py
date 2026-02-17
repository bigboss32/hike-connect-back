# inira/app/payments/infrastructure/input/payment_serializer.py

from rest_framework import serializers
from datetime import date


class ParticipantInputSerializer(serializers.Serializer):
    full_name = serializers.CharField(
        max_length=200,
        error_messages={
            "required": "El nombre completo es requerido",
            "blank": "El nombre no puede estar vacío",
        },
    )

    phone = serializers.CharField(
        max_length=20,
        error_messages={
            "required": "El teléfono es requerido",
            "blank": "El teléfono no puede estar vacío",
        },
    )

    emergency_contact_name = serializers.CharField(
        max_length=200,
        error_messages={
            "required": "El nombre del contacto de emergencia es requerido",
            "blank": "El nombre del contacto no puede estar vacío",
        },
    )

    emergency_contact_phone = serializers.CharField(
        max_length=20,
        error_messages={
            "required": "El teléfono de emergencia es requerido",
            "blank": "El teléfono de emergencia no puede estar vacío",
        },
    )

    def validate_phone(self, value):
        if value and not value.replace("+", "").replace(" ", "").isdigit():
            raise serializers.ValidationError("El teléfono debe contener solo números")
        return value

    def validate_emergency_contact_phone(self, value):
        if value and not value.replace("+", "").replace(" ", "").isdigit():
            raise serializers.ValidationError(
                "El teléfono de emergencia debe contener solo números"
            )
        return value


class ProcessPaymentInputSerializer(serializers.Serializer):
    # Ruta y reserva
    ruta_id = serializers.UUIDField(
        required=True,
        error_messages={
            "required": "La ruta es requerida",
            "invalid": "El ID de la ruta no es válido",
        },
    )

    booking_date = serializers.DateField(
        required=True,
        error_messages={
            "required": "La fecha de la excursión es requerida",
            "invalid": "Formato de fecha inválido. Use YYYY-MM-DD",
        },
    )

    # Participantes
    participants = serializers.ListField(
        child=ParticipantInputSerializer(),
        min_length=1,
        max_length=10,
        error_messages={
            "min_length": "Debe agregar al menos un participante",
            "max_length": "Máximo 10 participantes por reserva",
        },
    )

    # Wompi PSE
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
        choices=[0, 1],
        default=0,
        error_messages={
            "invalid_choice": "Tipo de usuario inválido. 0 = Persona natural, 1 = Persona jurídica"
        },
    )

    reference = serializers.CharField(
        required=False,
        max_length=255,
        allow_blank=True,
        help_text="Referencia del pago (opcional, se genera automáticamente)",
    )

    def validate_booking_date(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                "La fecha de la excursión debe ser futura"
            )
        return value

    def validate_user_legal_id(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("La cédula debe contener solo números")
        return value

    def validate_financial_institution_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("El código debe ser numérico")
        return value
