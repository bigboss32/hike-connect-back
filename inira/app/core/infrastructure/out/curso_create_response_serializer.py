from rest_framework import serializers


class CursoGoogleResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    shortname = serializers.CharField()
 

