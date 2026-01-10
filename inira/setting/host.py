import os

allowed_hosts = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

ALLOWED_HOSTS = [h.strip() for h in allowed_hosts if h.strip()]

# Obtener DEBUG del entorno
DEBUG = os.getenv("DJANGO_DEBUG", "false").strip().lower() == "true"

# CSRF_TRUSTED_ORIGINS desde el .env
csrf_origins_env = os.getenv("CSRF_TRUSTED_ORIGINS", "")
if csrf_origins_env:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_origins_env.split(",") if origin.strip()]
else:
    # Fallback: construir desde allowed_hosts
    CSRF_TRUSTED_ORIGINS = [
        f"https://{h.strip()}" for h in allowed_hosts
        if h.strip() not in ("localhost", "127.0.0.1")
    ]

# CORS_ALLOWED_ORIGINS desde el .env
cors_origins_env = os.getenv("CORS_ALLOWED_ORIGINS", "")

# Siempre definir CORS_ALLOWED_ORIGINS (nunca None)
if cors_origins_env:
    CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]
else:
    # Si no hay variable de entorno, usar lista vacía o construir desde allowed_hosts
    if DEBUG:
        # En desarrollo sin variable: lista vacía + CORS_ALLOW_ALL_ORIGINS
        CORS_ALLOWED_ORIGINS = []
    else:
        # En producción: construir desde allowed_hosts
        CORS_ALLOWED_ORIGINS = [
            f"https://{h.strip()}" for h in allowed_hosts
            if h.strip() not in ("localhost", "127.0.0.1")
        ]

# Permitir todos los orígenes solo en desarrollo sin configuración específica
if DEBUG and not cors_origins_env:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOW_ALL_ORIGINS = False

# Permitir credenciales
CORS_ALLOW_CREDENTIALS = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')