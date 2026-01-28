from rest_framework import serializers


class PostOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    author_name = serializers.CharField()
    author_image = serializers.CharField(allow_null=True)
