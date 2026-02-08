# inira/app/accounts/infrastructure/input/password_reset_serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User


class RequestPasswordResetSerializer(serializers.Serializer):
    """
    Serializer para solicitar código de recuperación de contraseña
    """

    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No existe una cuenta con este correo.")
        return value


class VerifyPasswordResetCodeSerializer(serializers.Serializer):
    """
    Serializer para verificar el código de recuperación
    """

    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer para establecer nueva contraseña
    """

    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirm = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Las contraseñas no coinciden"}
            )
        return data

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No existe una cuenta con este correo.")
        return value
