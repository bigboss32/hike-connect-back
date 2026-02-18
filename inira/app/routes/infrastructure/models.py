import uuid
from django.contrib.gis.db import models
from django.conf import settings
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import date


class RutaSenderismo(models.Model):
    """
    Modelo principal de rutas de senderismo.
    Contiene toda la información de la ruta y configuración de precios/disponibilidad.
    """

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

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rutas_creadas",
        help_text="Usuario que creó la ruta",
    )

    # Identificador único
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Información básica
    title = models.CharField(max_length=200, help_text="Nombre de la ruta")

    location = models.CharField(max_length=200, help_text="Ubicación de la ruta")

    distance = models.CharField(max_length=50, help_text="Distancia total (ej: 5.2 km)")

    duration = models.CharField(
        max_length=50, help_text="Duración estimada (ej: 3-4 horas)"
    )

    difficulty = models.CharField(
        max_length=10, choices=Dificultad.choices, help_text="Nivel de dificultad"
    )

    image = models.CharField(max_length=255, help_text="URL de la imagen principal")

    type = models.CharField(
        max_length=20, choices=Tipo.choices, help_text="Tipo de ruta"
    )

    company = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Empresa u organización a cargo",
    )

    category = models.CharField(
        max_length=20, choices=Categoria.choices, help_text="Categoría de la ruta"
    )

    description = models.TextField(help_text="Descripción detallada de la ruta")

    # PostGIS - Coordenadas geográficas
    coordinates = models.PointField(
        geography=True,
        spatial_index=True,
        help_text="Coordenadas GPS del punto de inicio",
    )

    # Información de contacto
    phone = models.CharField(max_length=20, help_text="Teléfono de contacto")

    email = models.EmailField(help_text="Email de contacto")

    whatsapp = models.CharField(max_length=20, help_text="Número de WhatsApp")

    # 🆕 Configuración de precios y pagos
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Precio base por persona en COP",
    )

    requires_payment = models.BooleanField(
        default=False, help_text="Si la ruta requiere pago previo para reservar"
    )

    # 🆕 Configuración de capacidad
    max_capacity = models.PositiveIntegerField(
        default=20,
        validators=[MinValueValidator(1)],
        help_text="Capacidad máxima de personas por excursión",
    )

    min_participants = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Mínimo de participantes requeridos por reserva",
    )

    max_participants_per_booking = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(1)],
        help_text="Máximo de participantes por reserva individual",
    )

    # 🆕 Configuración de disponibilidad
    requires_date_selection = models.BooleanField(
        default=True,
        help_text="Si se debe seleccionar fecha específica para la excursión",
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Si la ruta está disponible para reservas",
    )

    # 🆕 Información adicional
    included_services = models.TextField(
        blank=True, help_text="Servicios incluidos en el precio (separados por líneas)"
    )

    requirements = models.TextField(
        blank=True, help_text="Requisitos para los participantes"
    )

    what_to_bring = models.TextField(
        blank=True, help_text="Qué deben llevar los participantes"
    )

    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rutas_senderismo"
        ordering = ["-created_at"]
        verbose_name = "Ruta de Senderismo"
        verbose_name_plural = "Rutas de Senderismo"
        indexes = [
            models.Index(fields=["requires_payment", "is_active"]),
            models.Index(fields=["category", "type"]),
            models.Index(fields=["is_active", "created_at"]),
        ]

    def __str__(self):
        return self.title

    def calculate_price(self, number_of_people: int) -> Decimal:
        """
        Calcula el precio total según número de personas.

        Args:
            number_of_people: Número de participantes

        Returns:
            Precio total en COP
        """
        if number_of_people < 1:
            raise ValueError("El número de personas debe ser mayor a 0")

        return self.base_price * number_of_people

    def validate_booking_capacity(self, number_of_people: int):
        """
        Valida que se cumplan los límites de capacidad.

        Args:
            number_of_people: Número de participantes

        Raises:
            ValueError: Si no se cumplen los límites
        """
        if number_of_people < self.min_participants:
            raise ValueError(
                f"Se requieren mínimo {self.min_participants} participantes"
            )

        if number_of_people > self.max_participants_per_booking:
            raise ValueError(
                f"Máximo {self.max_participants_per_booking} participantes por reserva"
            )

    @property
    def has_pricing(self):
        """Verifica si la ruta tiene precio configurado"""
        return self.base_price > 0


class RutaRating(models.Model):
    """
    Calificaciones de rutas por usuarios.
    Un usuario solo puede calificar una ruta una vez.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    ruta = models.ForeignKey(
        RutaSenderismo, on_delete=models.CASCADE, related_name="ratings"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ruta_ratings"
    )

    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Calificación de 1 a 5 estrellas",
    )

    comment = models.TextField(
        blank=True, help_text="Comentario opcional sobre la experiencia"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("ruta", "user")
        db_table = "ruta_ratings"
        ordering = ["-created_at"]
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"
        indexes = [
            models.Index(fields=["ruta", "score"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.ruta.title} - {self.score}★ por {self.user.email}"


class RutaAvailability(models.Model):
    """
    Control de disponibilidad por fecha específica.
    Permite gestionar cupos disponibles para cada fecha de excursión.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    ruta = models.ForeignKey(
        RutaSenderismo, on_delete=models.CASCADE, related_name="availabilities"
    )

    date = models.DateField(help_text="Fecha de la excursión", db_index=True)

    available_slots = models.PositiveIntegerField(
        help_text="Cupos disponibles para esta fecha"
    )

    is_available = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Si está disponible para reservas esta fecha",
    )

    notes = models.TextField(
        blank=True, help_text="Notas especiales para esta fecha (ej: clima, eventos)"
    )

    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ruta_availabilities"
        unique_together = ("ruta", "date")
        ordering = ["date"]
        verbose_name = "Disponibilidad"
        verbose_name_plural = "Disponibilidades"
        indexes = [
            models.Index(fields=["ruta", "date"]),
            models.Index(fields=["date", "is_available"]),
            models.Index(fields=["is_available", "date"]),
        ]

    def __str__(self):
        return f"{self.ruta.title} - {self.date} ({self.available_slots} cupos)"

    @property
    def has_available_slots(self):
        """Verifica si hay cupos disponibles"""
        return self.is_available and self.available_slots > 0

    @property
    def is_past_date(self):
        """Verifica si la fecha ya pasó"""
        return self.date < date.today()

    def reserve_slots(self, number: int):
        """
        Reserva cupos para esta fecha.

        Args:
            number: Número de cupos a reservar

        Raises:
            ValueError: Si no hay suficientes cupos
        """
        if not self.is_available:
            raise ValueError("Esta fecha no está disponible para reservas")

        if self.is_past_date:
            raise ValueError("No se pueden reservar cupos en fechas pasadas")

        if self.available_slots < number:
            raise ValueError(f"Solo quedan {self.available_slots} cupos disponibles")

        self.available_slots -= number
        self.save(update_fields=["available_slots", "updated_at"])

    def release_slots(self, number: int):
        """
        Libera cupos cuando se cancela una reserva.

        Args:
            number: Número de cupos a liberar
        """
        original_capacity = self.ruta.max_capacity
        self.available_slots = min(self.available_slots + number, original_capacity)
        self.save(update_fields=["available_slots", "updated_at"])

    def mark_as_unavailable(self):
        """Marca esta fecha como no disponible"""
        self.is_available = False
        self.save(update_fields=["is_available", "updated_at"])

    def mark_as_available(self):
        """Marca esta fecha como disponible"""
        if not self.is_past_date:
            self.is_available = True
            self.save(update_fields=["is_available", "updated_at"])


class RutaImage(models.Model):
    """
    Galería de imágenes adicionales para cada ruta.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    ruta = models.ForeignKey(
        RutaSenderismo, on_delete=models.CASCADE, related_name="gallery_images"
    )

    image_url = models.CharField(max_length=500, help_text="URL de la imagen")

    caption = models.CharField(
        max_length=200, blank=True, help_text="Descripción de la imagen"
    )

    order = models.PositiveSmallIntegerField(
        default=0, help_text="Orden de visualización"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ruta_images"
        ordering = ["order", "created_at"]
        verbose_name = "Imagen de Ruta"
        verbose_name_plural = "Imágenes de Rutas"
        indexes = [
            models.Index(fields=["ruta", "order"]),
        ]

    def __str__(self):
        return f"{self.ruta.title} - Imagen {self.order}"
