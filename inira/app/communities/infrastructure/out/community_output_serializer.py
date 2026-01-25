# inira/app/communities/infrastructure/out/community_output_serializer.py

from rest_framework import serializers


class ComunidadOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    image = serializers.CharField()
    company = serializers.CharField(allow_null=True)
    location = serializers.CharField()
    is_public = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    member_count = serializers.IntegerField()
    user_is_member = serializers.BooleanField()


class ComunidadDetailOutputSerializer(ComunidadOutputSerializer):
    created_by_name = serializers.CharField()
    canales = serializers.ListField(default=[])  # Por ahora vacío, lo implementamos después