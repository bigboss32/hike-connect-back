FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias esenciales para PostgreSQL y desarrollo
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar y instalar dependencias de Python (incluyendo herramientas de dev)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install ipython debugpy

# Copiar código de la aplicación
COPY . .

# Exponer puerto para desarrollo
EXPOSE 8000

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]