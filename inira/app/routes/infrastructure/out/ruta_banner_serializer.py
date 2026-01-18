from rest_framework import serializers


class RutaBannerSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    image = serializers.CharField()

    difficulty = serializers.CharField()
    category = serializers.CharField()

    location = serializers.CharField()
    distance = serializers.CharField()
    duration = serializers.CharField()

    rating_avg = serializers.FloatField(allow_null=True)
    rating_count = serializers.IntegerField()
