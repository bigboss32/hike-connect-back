# inira/app/communities/admin.py

from django.contrib import admin
from .infrastructure.models import Comunidad, ComunidadMember, ComunidadCanal, ComunidadPost


@admin.register(Comunidad)
class ComunidadAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'location',
        'is_public',
        'created_by',
        'created_at',
        'member_count',
    )
    list_filter = ('is_public', 'created_at', 'location')
    search_fields = ('name', 'description', 'company', 'location')
    readonly_fields = ('id', 'created_at')
    
    fieldsets = (
        ('Información básica', {
            'fields': ('id', 'name', 'description', 'image')
        }),
        ('Detalles', {
            'fields': ('company', 'location', 'is_public')
        }),
        ('Creación', {
            'fields': ('created_by', 'created_at')
        }),
    )
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Miembros'


@admin.register(ComunidadMember)
class ComunidadMemberAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'comunidad',
        'role',
        'joined_at',
    )
    list_filter = ('role', 'joined_at')
    search_fields = ('user__username', 'user__email', 'comunidad__name')
    readonly_fields = ('id', 'joined_at')
    
    fieldsets = (
        ('Información', {
            'fields': ('id', 'comunidad', 'user', 'role')
        }),
        ('Fechas', {
            'fields': ('joined_at',)
        }),
    )


@admin.register(ComunidadCanal)
class ComunidadCanalAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'comunidad',
        'is_info',
        'is_read_only',
        'created_at',
        'post_count',
    )
    list_filter = ('is_info', 'is_read_only', 'created_at')
    search_fields = ('name', 'description', 'comunidad__name')
    readonly_fields = ('id', 'created_at')
    
    fieldsets = (
        ('Información básica', {
            'fields': ('id', 'comunidad', 'name', 'description')
        }),
        ('Configuración', {
            'fields': ('is_info', 'is_read_only')
        }),
        ('Fechas', {
            'fields': ('created_at',)
        }),
    )
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'


@admin.register(ComunidadPost)
class ComunidadPostAdmin(admin.ModelAdmin):
    list_display = (
        'short_content',
        'author',
        'canal',
        'comunidad',
        'created_at',
    )
    list_filter = ('created_at', 'canal__comunidad')
    search_fields = ('content', 'author__username', 'canal__name')
    readonly_fields = ('id', 'created_at')
    
    fieldsets = (
        ('Información', {
            'fields': ('id', 'comunidad', 'canal', 'author')
        }),
        ('Contenido', {
            'fields': ('content',)
        }),
        ('Fechas', {
            'fields': ('created_at',)
        }),
    )
    
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Contenido'