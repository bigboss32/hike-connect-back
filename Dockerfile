FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GUNICORN_WORKERS=4 \
    GUNICORN_THREADS=2 \
    GUNICORN_TIMEOUT=120 \
    PATH="$PATH:/opt/mssql-tools/bin"

WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    dos2unix \
    curl \
    bash \
    gnupg \
    unixodbc \
    unixodbc-dev \
    apt-transport-https \
    ca-certificates \
    && mkdir -p /usr/share/keyrings \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app

COPY --chown=appuser:appuser requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY --chown=appuser:appuser scripts/entrypoint.sh /app/scripts/entrypoint.sh
RUN dos2unix /app/scripts/entrypoint.sh && chmod +x /app/scripts/entrypoint.sh

COPY --chown=appuser:appuser . /app/

USER appuser

EXPOSE 8000

SHELL ["/bin/bash", "-c"]

ENTRYPOINT ["/bin/bash", "/app/scripts/entrypoint.sh"]

CMD gunicorn inira.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS} \
    --threads ${GUNICORN_THREADS} \
    --timeout ${GUNICORN_TIMEOUT} \
    --access-logfile - \
    --error-logfile - \
    --log-level info