# inira/app/communities/infrastructure/out/member_output_serializer.py

from rest_framework import serializers


class MemberOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    comunidad_id = serializers.UUIDField()
    user_id = serializers.IntegerField()
    user_name = serializers.CharField()
    user_image = serializers.CharField(allow_null=True)
    role = serializers.CharField()
    joined_at = serializers.DateTimeField()
