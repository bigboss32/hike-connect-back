from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UpdateProfileInputSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_first_name(self, value):
        """Validar que el nombre no esté vacío si se proporciona"""
        if value and not value.strip():
            raise serializers.ValidationError(_("El nombre no puede estar vacío"))
        return value.strip() if value else value
    
    def validate_last_name(self, value):
        """Validar que el apellido no esté vacío si se proporciona"""
        if value and not value.strip():
            raise serializers.ValidationError(_("El apellido no puede estar vacío"))
        return value.strip() if value else value

    def update(self, instance, validated_data):
        """Actualizar el usuario"""
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        
        # Si tu modelo User tiene campo 'bio', descomenta esto:
        # instance.bio = validated_data.get('bio', instance.bio)
        
        instance.save()
        return instance
    
    