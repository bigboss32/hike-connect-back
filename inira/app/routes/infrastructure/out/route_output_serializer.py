# inira/app/routes/infrastructure/out/route_output_serializer.py

from rest_framework import serializers
from inira.app.routes.domain.entities import RouteEntity


class CoordinatesOutputSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()


class RouteOutputSerializer(serializers.Serializer):
    # Campos originales
    id = serializers.UUIDField()
    title = serializers.CharField()
    location = serializers.CharField()
    distance = serializers.CharField()
    duration = serializers.CharField()
    difficulty = serializers.CharField()
    image = serializers.CharField()
    type = serializers.CharField()
    category = serializers.CharField()
    description = serializers.CharField()
    company = serializers.CharField(allow_null=True)
    phone = serializers.CharField(allow_null=True)
    email = serializers.EmailField(allow_null=True)
    whatsapp = serializers.CharField(allow_null=True)
    coordinates = CoordinatesOutputSerializer()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    # 🆕 Campos de pricing y configuración
    base_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, help_text="Precio base por persona en COP"
    )
    requires_payment = serializers.BooleanField(help_text="Si requiere pago previo")
    max_capacity = serializers.IntegerField(help_text="Capacidad máxima de personas")
    min_participants = serializers.IntegerField(
        help_text="Mínimo de participantes por reserva"
    )
    max_participants_per_booking = serializers.IntegerField(
        help_text="Máximo de participantes por reserva"
    )
    requires_date_selection = serializers.BooleanField(
        help_text="Si requiere selección de fecha"
    )
    is_active = serializers.BooleanField(help_text="Si está disponible para reservas")

    # 🆕 Información adicional
    included_services = serializers.CharField(
        allow_null=True, allow_blank=True, help_text="Servicios incluidos"
    )
    requirements = serializers.CharField(
        allow_null=True, allow_blank=True, help_text="Requisitos para participantes"
    )
    what_to_bring = serializers.CharField(
        allow_null=True, allow_blank=True, help_text="Qué deben traer los participantes"
    )

    # 🆕 Campos calculados (ratings)
    rating_avg = serializers.FloatField(
        allow_null=True, help_text="Promedio de calificaciones"
    )
    rating_count = serializers.IntegerField(help_text="Número total de calificaciones")
