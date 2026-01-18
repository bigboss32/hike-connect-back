from rest_framework import serializers


class RutaUserRatingSerializer(serializers.Serializer):
    ruta_id = serializers.UUIDField()
    score = serializers.IntegerField(allow_null=True)
