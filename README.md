# 📦 Proyecto Django con Arquitectura Hexagonal

Aplicación **Django** implementando **arquitectura hexagonal (ports & adapters)** con configuración lista para **Docker Compose** y desarrollo local.


# Construir la imagen desde el Dockerfile 
```
docker build -t registro-calificado-api .
```

# Verificar que la imagen se creó correctamente

```
docker images | grep registro-calificado-api 
docker images | findstr registro-calificado-api
```

# Ejecutar el contenedor con variables de entorno y mapeo de puertos
```
docker run --env-file .env -p 8000:8000 registro-calificado-api
```
---

## 🚀 Tecnologías principales

- [Python 3.11](https://www.python.org/)
- [Django 5](https://www.djangoproject.com/)
- [PostgreSQL 15](https://www.postgresql.org/)
- [MongoDB 6](https://www.mongodb.com/)
- [Docker & Docker Compose](https://docs.docker.com/)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
- [Pyrefly](https://pyrefly.dev/) - Análisis estático de tipos


## 📂 Estructura del proyecto

```
.
├── .devcontainer/                # Configuración para desarrollo en contenedor (VS Code Remote)
│   ├── devcontainer.json
│   └── Dockerfile
│
├── app/                          # Código fuente principal de Django
│   ├── Acta/                     # Módulo principal (puede haber más apps)
│   │   ├── application/          # Capa de aplicación (casos de uso, DTOs)
│   │   │   ├── dto.py
│   │   │   └── use_cases.py
│   │   │
│   │   ├── domain/               # Capa de dominio (reglas de negocio)
│   │   │   ├── entities.py       # Entidades de negocio puras (sin dependencias de Django)
│   │   │   ├── repositories.py   # Interfaces (ports) que definen cómo acceder a datos
│   │   │   ├── services.py       # Lógica de negocio (servicios de dominio)
│   │   │   └── value_objects.py  # Objetos de valor (tipados, invariantes)
│   │   │
│   │   ├── infrastructure/       # Capa de infraestructura (adapters)
│   │   │   ├── models.py         # Modelos Django (ORM)
│   │   │   ├── repositories.py   # Implementaciones concretas de repositorios
│   │   │   ├── serializers.py    # Serializadores de Django REST Framework
│   │   │   └── views.py          # Endpoints y vistas (adapters HTTP)
│   │   │
│   │   ├── migrations/           # Migraciones de base de datos
│   │   └── tests/                # Tests unitarios y de integración
│   │       ├── test_views.py
│   │       ├── test_models.py
│   │       └── ...
│   │
│   ├── Acuerdo/                  # Otra app de Django (ejemplo)
│   └── inira/      # Otra app de Django (ejemplo)
│
├── venv/                         # Entorno virtual local (si no se usa Docker)
│
├── .env                          # Variables de entorno (configuración sensible)
├── .gitignore
├── docker-compose.yml            # Orquestación con Docker Compose
├── Dockerfile                    # Imagen base para Django
├── entrypoint.sh                 # Script de arranque (migraciones + superusuario + servidor)
├── manage.py                     # Script de administración de Django
├── pyrefly.toml                  # Configuración de Pyrefly (tipado estático)
├── requirements.txt              # Dependencias Python
└── .pre-commit-config.yaml       # Hooks pre-commit (linting, formateo, etc.)
```

---

## ⚙️ Configuración inicial

### Variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Base de datos PostgreSQL
POSTGRES_DB=mi_db
POSTGRES_USER=mi_usuario
POSTGRES_PASSWORD=mi_password

# Django
DJANGO_SECRET_KEY=super-secret-key
DJANGO_DEBUG=True
DATABASE_URL=postgres://mi_usuario:mi_password@postgres:5432/mi_db

# Superusuario (creación automática)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin123
DJANGO_SUPERUSER_EMAIL=admin@example.com
```

> **Nota**: Para desarrollo local sin Docker, cambia `@postgres:5432` por `@localhost:5432` en `DATABASE_URL`.

---

## 🐳 Opción 1: Desarrollo con Docker Compose (Recomendado)

### Inicio rápido

```bash
# Construir y levantar todos los servicios
docker-compose up --build

# O en segundo plano
docker-compose up --build -d
```

El proyecto estará disponible en: **http://localhost:8000**

### Servicios incluidos

- **web-dev**: Contenedor Django con hot-reload
- **postgres**: PostgreSQL 15 con healthcheck
- **mongo**: MongoDB 6 con healthcheck

### Comandos útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f web-dev

# Ejecutar comandos Django
docker-compose exec web-dev python manage.py migrate
docker-compose exec web-dev python manage.py createsuperuser
docker-compose exec web-dev python manage.py test

# Abrir shell en el contenedor
docker-compose exec web-dev bash

# Reconstruir tras cambios en requirements.txt
docker-compose build web-dev
docker-compose up -d

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (⚠️ borra datos de BD)
docker-compose down -v
```

### Debugging con VS Code

El proyecto incluye configuración de debugpy. Para usarlo:

1. Modifica el comando en `docker-compose.yml`:
   ```yaml
   command: python -m debugpy --listen 0.0.0.0:5678 --wait-for-client manage.py runserver 0.0.0.0:8000
   ```

2. Conecta el depurador de VS Code al puerto `5678`

### Problemas comunes

| Problema | Solución |
|----------|----------|
| BD no responde | Espera el healthcheck: `docker-compose logs postgres` |
| Superusuario no se crea | Verifica variables `DJANGO_SUPERUSER_*` en `.env` |
| Cambios en dependencias no aplican | Reconstruye: `docker-compose build web-dev` |
| Puerto 8000 ocupado | Detén otros servicios o cambia el puerto en `docker-compose.yml` |

---

## 💻 Opción 2: Desarrollo local sin Docker

### 1. Requisitos del sistema

**Linux (Debian/Ubuntu)**
```bash
sudo apt-get update
sudo apt-get install -y python3-venv python3-dev build-essential libpq-dev
```

**macOS**
```bash
brew install postgresql python
```

**Windows**: Usa WSL2 o instala PostgreSQL y Python directamente.

### 2. Configurar entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar
source venv/bin/activate              # Linux/macOS
venv\Scripts\activate                 # Windows (cmd)
venv\Scripts\Activate.ps1             # Windows (PowerShell)
```

### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **Nota**: Si falla `psycopg2`, instala `libpq-dev` o usa `psycopg2-binary`.

### 4. Configurar PostgreSQL local

Actualiza `.env`:
```env
DATABASE_URL=postgres://mi_usuario:mi_password@localhost:5432/mi_db
```

Crea la base de datos:

```bash
# Opción 1: Con createdb
sudo -u postgres createuser mi_usuario
sudo -u postgres createdb mi_db -O mi_usuario

# Opción 2: Con psql
psql -U postgres -c "CREATE DATABASE mi_db;"
psql -U postgres -c "CREATE USER mi_usuario WITH PASSWORD 'mi_password';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE mi_db TO mi_usuario;"
```

### 5. Migraciones y datos iniciales

```bash
# Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

**Creación automática de superusuario** (opcional):

```bash
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_PASSWORD=admin123
export DJANGO_SUPERUSER_EMAIL=admin@example.com

python manage.py shell <<'EOF'
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")

if all([username, password, email]) and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password, email=email)
    print("✅ Superusuario creado")
else:
    print("ℹ️ Superusuario ya existe o faltan variables")
EOF
```

### 6. Ejecutar servidor

```bash
python manage.py runserver

# Para aceptar conexiones externas
python manage.py runserver 0.0.0.0:8000
```

Accede a:
- **Aplicación**: http://127.0.0.1:8000
- **Admin**: http://127.0.0.1:8000/admin

### Problemas comunes

| Problema | Solución |
|----------|----------|
| Error al instalar `psycopg2` | Instala `libpq-dev` o usa `psycopg2-binary` |
| PostgreSQL no conecta | Verifica servicio: `systemctl status postgresql` |
| Variables de entorno no cargan | Usa `export` o configura django-environ |

---

## 🧪 Testing y calidad de código

### Ejecutar tests

```bash
# Con Docker
docker-compose exec web-dev python manage.py test

# Local
python manage.py test
```

### Análisis estático con Pyrefly

```bash
pip install pyrefly
pyrefly check
```

### Pre-commit hooks

```bash
pip install pre-commit
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files
```

---

## 📝 Cheatsheet de comandos

### Docker

```bash
docker-compose up --build -d              # Levantar en background
docker-compose logs -f web-dev            # Ver logs
docker-compose exec web-dev bash          # Shell en contenedor
docker-compose exec web-dev python manage.py [comando]
docker-compose down -v                    # Detener y limpiar
```

### Django (local)

```bash
python manage.py migrate                  # Aplicar migraciones
python manage.py createsuperuser          # Crear admin
python manage.py runserver                # Iniciar servidor
python manage.py test                     # Ejecutar tests
python manage.py shell                    # Shell interactivo
python manage.py collectstatic            # Archivos estáticos
```

### Calidad de código

```bash
pyrefly check                             # Análisis de tipos
pre-commit run --all-files                # Ejecutar hooks
python manage.py test                     # Suite de tests
```

---

## 📚 Recursos adicionales

- [Documentación Django](https://docs.djangoproject.com/)
- [Arquitectura Hexagonal](https://alistair.cockburn.us/hexagonal-architecture/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Pyrefly](https://pyrefly.dev/)

---

## 🤝 Contribución

1. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
2. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
3. Push a la rama (`git push origin feature/AmazingFeature`)
4. Abre un Pull Request

---

