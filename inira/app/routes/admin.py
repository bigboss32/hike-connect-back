# inira/app/rutas/admin.py

from django.contrib import admin
from .models import RutaSenderismo, RutaRating, RutaAvailability, RutaImage
from django.contrib.gis.admin import GISModelAdmin


@admin.register(RutaSenderismo)
class RutaSenderismoAdmin(GISModelAdmin):
    list_display = [
        "title",
        "location",
        "difficulty",
        "category",
        "base_price",
        "requires_payment",
        "is_active",
        "created_at",
    ]
    list_filter = [
        "difficulty",
        "type",
        "category",
        "requires_payment",
        "is_active",
    ]
    search_fields = ["title", "location", "company"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(RutaRating)
class RutaRatingAdmin(admin.ModelAdmin):
    list_display = ["ruta", "user", "score", "created_at"]
    list_filter = ["score", "created_at"]
    search_fields = ["ruta__title", "user__email"]


@admin.register(RutaAvailability)
class RutaAvailabilityAdmin(admin.ModelAdmin):
    list_display = [
        "ruta",
        "date",
        "available_slots",
        "is_available",
        "created_at",
    ]
    list_filter = ["is_available", "date"]
    search_fields = ["ruta__title"]


@admin.register(RutaImage)
class RutaImageAdmin(admin.ModelAdmin):
    list_display = ["ruta", "caption", "order", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["ruta__title", "caption"]
