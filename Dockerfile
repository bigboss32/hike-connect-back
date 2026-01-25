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
# RUNTIME — imagen final
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

# ✅ Crear entrypoint que ejecuta migraciones directamente
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

CMD ["gunicorn", "inira.wsgi:application", \
     "--bind=0.0.0.0:8000", \
     "--workers=4", \
     "--timeout=120", \
     "--access-logfile=-", \
     "--error-logfile=-", \
     "--log-level=info"]