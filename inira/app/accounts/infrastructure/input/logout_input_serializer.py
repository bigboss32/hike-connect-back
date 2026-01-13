from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class LogoutInputSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        help_text="Token de actualización (refresh token) a invalidar"
    )