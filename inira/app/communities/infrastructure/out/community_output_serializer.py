# inira/app/communities/infrastructure/out/community_output_serializer.py

from rest_framework import serializers

from inira.app.communities.infrastructure.models import Comunidad



class ComunidadOutputSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    user_is_member = serializers.SerializerMethodField()

    class Meta:
        model = Comunidad
        fields = [
            "id",
            "name",
            "description",
            "image",
            "company",
            "location",
            "is_public",
            "created_at",
            "member_count",
            "user_is_member",
        ]

    def get_member_count(self, obj):
        return obj.members.count()

    def get_user_is_member(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.members.filter(user=request.user).exists()
        return False


class ComunidadDetailOutputSerializer(ComunidadOutputSerializer):
    canales = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()

    class Meta(ComunidadOutputSerializer.Meta):
        fields = ComunidadOutputSerializer.Meta.fields + [
            "canales",
            "created_by_name",
        ]

    def get_canales(self, obj):
        from inira.app.communities.infrastructure.out.channel_output_serializer import (
            CanalOutputSerializer
        )
        return CanalOutputSerializer(obj.canales.all(), many=True).data

    def get_created_by_name(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"