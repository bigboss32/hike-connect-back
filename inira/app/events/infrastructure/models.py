# inira/app/events/infrastructure/models.py

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models


class Evento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)

    max_participants = models.PositiveIntegerField()

    # 👤 Organizador
    organized_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="eventos_organizados"
    )

    # 📍 Punto de reunión (PostGIS)
    meeting_point = models.PointField(
        geography=True,
        spatial_index=True,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)


class EventoInscripcion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name="inscripciones"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="eventos_inscritos"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("evento", "user")
