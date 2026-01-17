from rest_framework import serializers
from inira.app.routes.domain.entities import RouteEntity

class CoordinatesOutputSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()

    
class RouteOutputSerializer(serializers.Serializer):
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
    phone = serializers.CharField()
    email = serializers.EmailField()
    whatsapp = serializers.CharField()

    coordinates = CoordinatesOutputSerializer()

    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


