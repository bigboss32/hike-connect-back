from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UpdateProfileInputSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(max_length=500, required=False, allow_blank=True)
    avatar = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    
    def validate_first_name(self, value):
        if value and not value.strip():
            raise serializers.ValidationError(_("El nombre no puede estar vacío"))
        return value.strip() if value else value
    
    def validate_last_name(self, value):
        if value and not value.strip():
            raise serializers.ValidationError(_("El apellido no puede estar vacío"))
        return value.strip() if value else value

    def update(self, instance, validated_data):
        """Actualizar usuario y perfil"""
        # Actualizar campos del User
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        
        # Actualizar campos del Profile
        profile = instance.profile
        profile.bio = validated_data.get('bio', profile.bio)
        profile.avatar = validated_data.get('avatar', profile.avatar)
        profile.save()
        
        return instance