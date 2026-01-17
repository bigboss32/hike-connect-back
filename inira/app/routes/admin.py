from django.contrib import admin

from django.contrib.gis.admin import GISModelAdmin
from django.contrib.gis.db import models

from .models import RutaSenderismo


@admin.register(RutaSenderismo)
class RutaSenderismoAdmin(GISModelAdmin):
    list_display = (
        "title",
        "difficulty",
        "distance",
        "type",
        "category",
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
    )

    formfield_overrides = {
        models.PointField: {
            "widget": admin.widgets.AdminTextareaWidget(
                attrs={"rows": 1, "cols": 40}
            )
        }
    }