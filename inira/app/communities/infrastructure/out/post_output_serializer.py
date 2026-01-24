# inira/app/communities/infrastructure/out/post_output_serializer.py

from rest_framework import serializers

from inira.app.communities.infrastructure.models import ComunidadPost



class PostOutputSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    author_image = serializers.SerializerMethodField()

    class Meta:
        model = ComunidadPost
        fields = [
            "id",
            "content",
            "created_at",
            "author_name",
            "author_image",
        ]

    def get_author_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"

    def get_author_image(self, obj):
        return getattr(obj.author, "profile_image", None)