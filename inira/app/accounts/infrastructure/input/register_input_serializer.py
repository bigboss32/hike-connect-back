from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class RegisterInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    def validate_email(self, value):
        """Verificar que el email no esté registrado"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("Este email ya está registrado"))
        return value.lower()

    def validate(self, attrs):
        """Validar que las contraseñas coincidan"""
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": _("Las contraseñas no coinciden")}
            )

        return attrs

    def create(self, validated_data):
        """Crear el usuario con email como username"""
        validated_data.pop("password_confirm")
        
        # Usar email como username
        user = User.objects.create_user(
            username=validated_data["email"],  # ← Email como username
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        
        return user