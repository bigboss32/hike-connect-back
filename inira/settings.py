import os
from pathlib import Path
from datetime import timedelta

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

WSGI_APPLICATION = "inira.wsgi.application"

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
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Course Sync Service API',
    'DESCRIPTION': (
        "Course Sync Service API es un servicio que actúa como un puente de "
        "integración entre SINU y Google Classroom, permitiendo la creación, "
        "actualización y administración automatizada de cursos académicos. "
        "La API sincroniza información institucional como asignaturas, docentes, "
        "estudiantes y grupos, para generar aulas virtuales en Classroom de manera "
        "segura, consistente y sin intervención manual."
    ),
     "TAGS": [
        {
            "name": "Core API",
            "description": (
                "Grupo de operaciones que interactúan con los Web Services de Moodle. "
                "Incluye creación, actualización, consulta y eliminación de cursos."
            ),
        },
    ],
    'VERSION': '1.0.0',
}
