FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install ipython debugpy

COPY . .

# 🔥 FIX CRÍTICO
RUN dos2unix .devcontainer/entrypoint_dev.sh \
    && chmod +x .devcontainer/entrypoint_dev.sh

EXPOSE 8000

ENTRYPOINT ["/bin/bash", "/app/.devcontainer/entrypoint_dev.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]