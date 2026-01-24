# inira/app/communities/models.py

import uuid
from django.db import models
from django.conf import settings


class Comunidad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=200)
    description = models.TextField()

    image = models.CharField(max_length=255)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="communities_created"
    )

    company = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=200
    )

    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comunidades"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class ComunidadMember(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        MEMBER = "member", "Member"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    comunidad = models.ForeignKey(
        Comunidad,
        on_delete=models.CASCADE,
        related_name="members"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="community_memberships"
    )

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.MEMBER
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("comunidad", "user")
        db_table = "comunidad_members"



class ComunidadCanal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    comunidad = models.ForeignKey(
        Comunidad,
        on_delete=models.CASCADE,
        related_name="canales"
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    is_info = models.BooleanField(default=False)  
    is_read_only = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comunidad_canales"
        unique_together = ("comunidad", "name")

    def __str__(self):
        return f"{self.comunidad.name} - {self.name}"


class ComunidadPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    comunidad = models.ForeignKey(
        Comunidad,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    canal = models.ForeignKey(
        ComunidadCanal,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="community_posts"
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comunidad_posts"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author} - {self.content[:30]}"
