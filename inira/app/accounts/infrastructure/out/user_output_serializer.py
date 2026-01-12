from rest_framework import serializers


class UserOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        """Retorna nombre completo"""
        return f"{obj.get('first_name', '')} {obj.get('last_name', '')}".strip()