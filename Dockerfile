FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copiar código
COPY . .

# Collectstatic
RUN python manage.py collectstatic --noinput || true

SHELL ["/bin/bash", "-c"]

ENTRYPOINT ["/bin/bash", "/app/scripts/entrypoint.sh"]

# Render asigna PORT automáticamente (por defecto 10000)
CMD gunicorn inira.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
