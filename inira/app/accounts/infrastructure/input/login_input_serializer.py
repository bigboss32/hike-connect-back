from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from inira.app.accounts.infrastructure.models import Profile


class LoginInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        User = get_user_model()
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": _("Credenciales inválidas")})
        user = authenticate(username=user_obj.username, password=password)
        if not user:
            raise serializers.ValidationError({"detail": _("Credenciales inválidas")})
        if not user.profile.correo_electronico_confirmado:
            raise serializers.ValidationError(
                {"detail": _("Debes verificar tu correo antes de iniciar sesión.")}
            )

        attrs["user"] = user
        return attrs
