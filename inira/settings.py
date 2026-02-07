import os
from pathlib import Path
from datetime import timedelta
from decouple import config
from inira.setting.paths import *
from inira.setting.databases import DATABASES
from inira.setting.logging import LOGGING
from inira.setting.apps import INSTALLED_APPS
from inira.setting.host import (
    ALLOWED_HOSTS,
    CSRF_TRUSTED_ORIGINS,
    CORS_ALLOWED_ORIGINS,
    CORS_ALLOW_ALL_ORIGINS,
    CORS_ALLOW_CREDENTIALS,
    SECURE_PROXY_SSL_HEADER
)



SECRET_KEY = os.getenv("SECRET_KEY", "false")
DEBUG = os.getenv("DJANGO_DEBUG", "False").strip().lower() == "true"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",  
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "inira.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ===============================
# ASGI / CHANNELS
# ===============================
ASGI_APPLICATION = "inira.asgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-es"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
}
SPECTACULAR_SETTINGS = {
    'TITLE': 'API de Senderismo Hike Connect',
    'DESCRIPTION': (
        "API REST para la gestión integral de rutas de senderismo. "
        "Permite la creación, consulta, actualización y administración de rutas, "
        "perfiles de usuario, experiencias y actividades relacionadas con senderismo."
    ),
    'VERSION': '1.0.0',
    
    'LANGUAGE': 'es',
    
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    
    'SECURITY': [{'Bearer': []}],
    'APPEND_COMPONENTS': {
        'securitySchemes': {
            'Bearer': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
                'description': 'Ingrese el token JWT en el formato: Bearer <token>'
            }
        }
    },
    
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': False,
        'filter': True,
        'defaultModelsExpandDepth': 1,
        'defaultModelExpandDepth': 1,
        'tagsSorter': 'alpha',  # Ordena alfabéticamente
        'operationsSorter': 'alpha',
    },
    
    'TAGS': [
        {
            'name': 'Autenticación',
            'description': 'Endpoints para autenticación de usuarios (login, registro, renovación de tokens)',
        },
        {
            'name': 'Usuarios',
            'description': 'Gestión de perfiles de usuario y preferencias',
        },
        {
            'name': 'Rutas',
            'description': 'Operaciones CRUD para rutas de senderismo',
        },
        {
            'name': 'Eventos',
            'description': 'Gestión de experiencias y reseñas de rutas',
        },
        {
            'name': 'Comunidades - Gestión',
            'description': 'Crear y consultar comunidades',
        },
        {
            'name': 'Comunidades - Miembros',
            'description': 'Gestión de membresías en comunidades',
        },
        {
            'name': 'Comunidades - Canales',
            'description': 'Gestión de canales dentro de comunidades',
        },
        {
            'name': 'Comunidades - Posts',
            'description': 'Gestión de publicaciones en canales',
        },
    ],
    
    'CONTACT': {
        'name': 'Equipo de Desarrollo',
        'email': 'soporte@hikeconnect.com',
    },
    'LICENSE': {
        'name': 'MIT License',
    },
    
    'EXTERNAL_DOCS': {
        'description': 'Documentación completa',
        'url': 'https://docs.hikeconnect.com',
    },
}

MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [config("REDIS_URL")],
        },
    },
}
