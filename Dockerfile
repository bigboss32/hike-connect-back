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

RUN addgroup --system django \
    && adduser --system --ingroup django django \
    && chown -R django:django /app

USER django

EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=inira.settings

# ✅ SOLUCIÓN: Gunicorn arranca PRIMERO, migraciones en background
CMD ["sh", "-c", "\
echo '🌐 Iniciando Gunicorn...' && \
gunicorn inira.wsgi:application \
  --bind=0.0.0.0:${PORT:-8000} \
  --workers=${WEB_CONCURRENCY:-1} \
  --timeout=120 \
  --access-logfile=- \
  --error-logfile=- \
  --log-level=info \
  --preload & \
GUNICORN_PID=$! && \
echo '🔍 Esperando PostgreSQL...' && \
max_attempts=30 && \
attempt=0 && \
until python manage.py migrate --check 2>/dev/null || [ $attempt -eq $max_attempts ]; do \
  attempt=$((attempt + 1)); \
  echo \"Intento $attempt/$max_attempts\"; \
  sleep 1; \
done && \
if [ $attempt -eq $max_attempts ]; then \
  echo '❌ DB timeout'; \
  kill $GUNICORN_PID; \
  exit 1; \
fi && \
echo '🚀 Aplicando migraciones...' && \
python manage.py migrate --noinput && \
echo '✅ Migraciones completas' && \
wait $GUNICORN_PID \
"]