from rest_framework import serializers


class UserOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    full_name = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        """Retorna nombre completo"""
        first = obj.get('first_name', '')
        last = obj.get('last_name', '')
        return f"{first} {last}".strip()
    
    def get_bio(self, obj):
        """Retorna biografía del perfil"""
        return obj.get('bio', '')
    
    def get_avatar(self, obj):
        """Retorna URL del avatar"""
        return obj.get('avatar', None)