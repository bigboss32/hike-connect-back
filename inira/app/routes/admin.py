from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django.contrib.gis.db import models
from django.db.models import Avg, Count

from .models import RutaSenderismo, RutaRating


@admin.register(RutaSenderismo)
class RutaSenderismoAdmin(GISModelAdmin):
    list_display = (
        "title",
        "difficulty",
        "distance",
        "type",
        "category",
        "rating_avg",
        "rating_count",
        "created_at",
    )

    list_filter = (
        "difficulty",
        "type",
        "category",
    )

    search_fields = (
        "title",
        "location",
        "description",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "rating_avg",
        "rating_count",
    )

    formfield_overrides = {
        models.PointField: {
            "widget": admin.widgets.AdminTextareaWidget(
                attrs={"rows": 1, "cols": 40}
            )
        }
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _rating_avg=Avg("ratings__score"),
            _rating_count=Count("ratings"),
        )

    @admin.display(description="⭐ Rating promedio", ordering="_rating_avg")
    def rating_avg(self, obj):
        return round(obj._rating_avg, 2) if obj._rating_avg else "—"

    @admin.display(description="🧮 Nº ratings", ordering="_rating_count")
    def rating_count(self, obj):
        return obj._rating_count
