FROM python:3.11-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    GDAL_LIBRARY_PATH=/usr/lib/libgdal.so \
    GEOS_LIBRARY_PATH=/usr/lib/libgeos_c.so

# Instalación más limpia sin dos2unix
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

COPY . .

# Solo aseguramos permisos de ejecución (sin dos2unix)
RUN if [ -f ".devcontainer/entrypoint_dev.sh" ]; then \
        chmod +x .devcontainer/entrypoint_dev.sh; \
    fi

EXPOSE 8000

ENTRYPOINT ["/bin/bash", "/app/.devcontainer/entrypoint_dev.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]