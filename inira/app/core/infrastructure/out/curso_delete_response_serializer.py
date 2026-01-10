from rest_framework import serializers


class CursoDeleteResponseSerializer(serializers.Serializer):
    course_id = serializers.CharField()
    status = serializers.CharField()
    message = serializers.CharField()