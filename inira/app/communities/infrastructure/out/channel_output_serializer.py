# inira/app/communities/infrastructure/out/channel_output_serializer.py

from rest_framework import serializers


class CanalOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    is_info = serializers.BooleanField()
    is_read_only = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    post_count = serializers.IntegerField()
