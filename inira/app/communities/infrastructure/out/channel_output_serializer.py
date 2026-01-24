# inira/app/communities/infrastructure/out/channel_output_serializer.py

from rest_framework import serializers

from inira.app.communities.infrastructure.models import ComunidadCanal


class CanalOutputSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = ComunidadCanal
        fields = [
            "id",
            "name",
            "description",
            "is_info",
            "is_read_only",
            "created_at",
            "post_count",
        ]

    def get_post_count(self, obj):
        return obj.posts.count()