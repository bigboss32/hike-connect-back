from rest_framework import serializers

from inira.app.routes.infrastructure.models import RutaSenderismo



class RutaSenderismoSerializer(serializers.ModelSerializer):
    coordinates = serializers.SerializerMethodField()

    class Meta:
        model = RutaSenderismo
        fields = [
            "id",
            "title",
            "location",
            "distance",
            "duration",
            "difficulty",
            "image",
            "type",
            "company",
            "category",
            "description",
            "coordinates",
            "phone",
            "email",
            "whatsapp",
            "created_at",
        ]

    def get_coordinates(self, obj):
        if obj.coordinates:
            return {
                "lat": obj.coordinates.y,
                "lng": obj.coordinates.x,
            }
        return None
