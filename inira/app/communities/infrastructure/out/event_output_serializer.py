from rest_framework import serializers


class CoordinatesSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()


class EventOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    date = serializers.DateTimeField()
    location = serializers.CharField()

    max_participants = serializers.IntegerField()
    participants_count = serializers.IntegerField()

    organized_by = serializers.CharField(allow_null=True)

    meeting_point = serializers.SerializerMethodField()

    def get_meeting_point(self, obj):
        if obj.meeting_point_lat is None or obj.meeting_point_lng is None:
            return None

        return {
            "lat": obj.meeting_point_lat,
            "lng": obj.meeting_point_lng,
        }
