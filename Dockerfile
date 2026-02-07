# =============================
# DEV — desarrollo local
# =============================
FROM python:3.11-slim-bookworm AS dev

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    GDAL_LIBRARY_PATH=/usr/lib/libgdal.so \
    GEOS_LIBRARY_PATH=/usr/lib/libgeos_c.so

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt ipython debugpy

# No copiamos código aquí (viene del volumen)
# No creamos entrypoint (viene del docker-compose command)

EXPOSE 8000


# =============================
# BUILDER — compila wheels
# =============================
FROM python:3.11-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libgdal-dev \
    libgeos-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir -r requirements.txt


# =============================
# RUNTIME — producción (default)
# =============================
FROM python:3.11-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONOPTIMIZE=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    gdal-bin \
    libgdal32 \
    libgeos-c1v5 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /build /wheels
RUN pip install --no-cache-dir /wheels/*.whl && rm -rf /wheels /root/.cache

COPY . .

RUN python manage.py collectstatic --noinput || true

RUN echo '#!/bin/sh\n\
set -e\n\
\n\
echo "🚀 Aplicando migraciones..."\n\
python manage.py migrate --noinput\n\
\n\
echo "✅ Migraciones aplicadas"\n\
\n\
exec "$@"\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

RUN addgroup --system django \
    && adduser --system --ingroup django django \
    && chown -R django:django /app

USER django

EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=inira.settings

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["sh", "-c", "daphne -b 0.0.0.0 -p $PORT inira.asgi:application"]

