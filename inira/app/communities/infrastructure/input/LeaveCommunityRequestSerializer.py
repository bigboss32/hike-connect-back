# inira/app/communities/infrastructure/input.py

from rest_framework import serializers


class LeaveCommunityRequestSerializer(serializers.Serializer):
    comunidad_id = serializers.UUIDField(
        required=True,
        help_text="ID UUID de la comunidad que se desea abandonar"
    )

    class Meta:
        ref_name = "LeaveCommunityRequest"


class JoinCommunityRequestSerializer(serializers.Serializer):
    comunidad_id = serializers.UUIDField(
        required=True,
        help_text="ID UUID de la comunidad a la que se desea unir"
    )

    class Meta:
        ref_name = "JoinCommunityRequest"


class CreateChannelRequestSerializer(serializers.Serializer):
    comunidad_id = serializers.UUIDField(
        required=True,
        help_text="ID UUID de la comunidad donde se creará el canal"
    )
    name = serializers.CharField(
        required=True,
        max_length=100,
        help_text="Nombre del canal"
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Descripción del canal"
    )
    is_info = serializers.BooleanField(
        required=False,
        default=False,
        help_text="Indica si es un canal informativo"
    )
    is_read_only = serializers.BooleanField(
        required=False,
        default=False,
        help_text="Indica si el canal es de solo lectura"
    )

    class Meta:
        ref_name = "CreateChannelRequest"


class CreatePostRequestSerializer(serializers.Serializer):
    comunidad_id = serializers.UUIDField(
        required=True,
        help_text="ID UUID de la comunidad"
    )
    canal_id = serializers.UUIDField(
        required=True,
        help_text="ID UUID del canal donde se publicará"
    )
    content = serializers.CharField(
        required=True,
        help_text="Contenido del post"
    )

    class Meta:
        ref_name = "CreatePostRequest"


class CreateCommunityRequestSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True,
        max_length=200,
        help_text="Nombre de la comunidad"
    )
    description = serializers.CharField(
        required=True,
        help_text="Descripción de la comunidad"
    )
    image = serializers.CharField(
        required=True,
        max_length=255,
        help_text="URL de la imagen de la comunidad"
    )
    company = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        max_length=200,
        help_text="Empresa asociada (opcional)"
    )
    location = serializers.CharField(
        required=True,
        max_length=200,
        help_text="Ubicación de la comunidad"
    )
    is_public = serializers.BooleanField(
        required=False,
        default=True,
        help_text="Define si la comunidad es pública o privada"
    )

    class Meta:
        ref_name = "CreateCommunityRequest"