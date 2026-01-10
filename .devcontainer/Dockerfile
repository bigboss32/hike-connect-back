FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    bash \
    dos2unix \
    git \
    ssh \
    gnupg \
    unixodbc \
    unixodbc-dev \
    apt-transport-https \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/share/keyrings && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="$PATH:/opt/mssql-tools/bin"

COPY .devcontainer/entrypoint_dev.sh /app/.devcontainer/entrypoint_dev.sh
RUN dos2unix /app/.devcontainer/entrypoint_dev.sh && chmod +x /app/.devcontainer/entrypoint_dev.sh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install ipython debugpy

COPY . .

EXPOSE 8000

SHELL ["/bin/bash", "-c"]

ENTRYPOINT ["/bin/bash", "/app/.devcontainer/entrypoint_dev.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]