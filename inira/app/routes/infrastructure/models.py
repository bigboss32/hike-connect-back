
# Create your models here.


import uuid
from django.contrib.gis.db import models
from django.conf import settings

class RutaSenderismo(models.Model):
    class Dificultad(models.TextChoices):
        FACIL = "Fácil", "Fácil"
        MEDIO = "Medio", "Medio"
        DIFICIL = "Difícil", "Difícil"

    class Tipo(models.TextChoices):
        PUBLICA = "pública", "Pública"
        PRIVADA = "privada", "Privada"
        AGROTURISMO = "agroturismo", "Agroturismo"

    class Categoria(models.TextChoices):
        SENDERISMO = "senderismo", "Senderismo"
        AGROTURISMO = "agroturismo", "Agroturismo"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    distance = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)

    difficulty = models.CharField(
        max_length=10,
        choices=Dificultad.choices
    )

    image = models.CharField(max_length=255)

    type = models.CharField(
        max_length=20,
        choices=Tipo.choices
    )

    company = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    category = models.CharField(
        max_length=20,
        choices=Categoria.choices
    )

    description = models.TextField()

    # 🔥 PostGIS
    coordinates = models.PointField(
        geography=True,
        spatial_index=True
    )

    # Contacto
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rutas_senderismo"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class RutaRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    ruta = models.ForeignKey(
        RutaSenderismo,
        on_delete=models.CASCADE,
        related_name="ratings"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ruta_ratings"
    )

    score = models.PositiveSmallIntegerField()  # 1 a 5

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("ruta", "user")
        db_table = "ruta_ratings"

    def __str__(self):
        return f"{self.ruta.title} - {self.score}"