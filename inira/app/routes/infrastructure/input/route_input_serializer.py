from rest_framework import serializers
from uuid import UUID


class CoordinatesInputSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()


class RouteInputSerializer(serializers.Serializer):
    # Obligatorios
    title = serializers.CharField(max_length=200)
    location = serializers.CharField(max_length=200)
    distance = serializers.CharField(max_length=50)
    duration = serializers.CharField(max_length=50)
    difficulty = serializers.ChoiceField(choices=["Fácil", "Medio", "Difícil"])
    image = serializers.CharField(max_length=255)
    type = serializers.ChoiceField(choices=["pública", "privada", "agroturismo"])
    category = serializers.ChoiceField(choices=["senderismo", "agroturismo"])
    description = serializers.CharField()
    coordinates = CoordinatesInputSerializer()
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    whatsapp = serializers.CharField(max_length=20)

    # 👇 company ahora incluida como opcional
    company = serializers.CharField(
        max_length=200, required=False, allow_null=True, allow_blank=True
    )

    # Pricing
    base_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, default="0.00", min_value=0
    )
    requires_payment = serializers.BooleanField(required=False, default=False)
    max_capacity = serializers.IntegerField(required=False, default=20, min_value=1)
    min_participants = serializers.IntegerField(required=False, default=1, min_value=1)
    max_participants_per_booking = serializers.IntegerField(
        required=False, default=10, min_value=1
    )
    requires_date_selection = serializers.BooleanField(required=False, default=True)
    is_active = serializers.BooleanField(required=False, default=True)

    # Info adicional
    included_services = serializers.CharField(
        required=False, allow_blank=True, default=""
    )
    requirements = serializers.CharField(required=False, allow_blank=True, default="")
    what_to_bring = serializers.CharField(required=False, allow_blank=True, default="")
