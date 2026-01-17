FROM python:3.11-slim

WORKDIR /app

# 🔥 DEPENDENCIAS DEL SISTEMA (PostGIS / GDAL / PROJ + Git)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    curl \
    dos2unix \
    git \
    && rm -rf /var/lib/apt/lists/*

# 🔥 Variables para que Django encuentre GDAL y GEOS
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
ENV GEOS_LIBRARY_PATH=/usr/lib/libgeos_c.so

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install ipython debugpy

COPY . .

# 🔥 FIX CRÍTICO (lo conservamos)
RUN dos2unix .devcontainer/entrypoint_dev.sh \
    && chmod +x .devcontainer/entrypoint_dev.sh

EXPOSE 8000

ENTRYPOINT ["/bin/bash", "/app/.devcontainer/entrypoint_dev.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]