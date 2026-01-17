from rest_framework import serializers
from inira.app.accounts.infrastructure.out.user_output_serializer import UserOutputSerializer


class LoginOutputSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserOutputSerializer()
