from rest_framework import serializers
from uuid import UUID


class RutaRatingInputSerializer(serializers.Serializer):
    ruta_id = serializers.UUIDField(
        help_text="ID de la ruta a calificar"
    )
    score = serializers.IntegerField(
        min_value=1,
        max_value=5,
        help_text="Puntuación de la ruta (1 a 5)"
    )
