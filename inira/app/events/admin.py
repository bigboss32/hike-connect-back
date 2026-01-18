from django.contrib import admin
from .models import Evento, EventoInscripcion
from django.contrib.gis.admin import GISModelAdmin

@admin.register(Evento)
class EventoAdmin(GISModelAdmin):
    list_display = (
        "title",
        "date",
        "location",
        "max_participants",
        "participants_count",
        "created_at",
    )
    list_filter = ("date", "location")
    search_fields = ("title", "location")
    ordering = ("-date",)

    def participants_count(self, obj):
        return obj.inscripciones.count()

    participants_count.short_description = "Inscritos"


@admin.register(EventoInscripcion)
class EventoInscripcionAdmin(admin.ModelAdmin):
    list_display = (
        "evento",
        "user",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "evento__title",
        "user__username",
        "user__email",
    )
    autocomplete_fields = ("evento", "user")
    ordering = ("-created_at",)
