#!/bin/bash
set -e

echo "=== 🚀 Iniciando entorno local de desarrollo ==="

echo "📦 Variables de entorno detectadas:"
echo "POSTGRES_HOST=${POSTGRES_HOST}"
echo "POSTGRES_DB=${POSTGRES_DB}"
echo "POSTGRES_USER=${POSTGRES_USER}"

# ===============================
# Esperar a PostgreSQL
# ===============================
echo "📊 Verificando PostgreSQL..."

MAX_TRIES=30
TRIES=0

until python - <<EOF
import psycopg2
psycopg2.connect(
    host="${POSTGRES_HOST}",
    user="${POSTGRES_USER}",
    password="${POSTGRES_PASSWORD}",
    dbname="${POSTGRES_DB}",
)
EOF
do
  TRIES=$((TRIES+1))
  if [ "$TRIES" -ge "$MAX_TRIES" ]; then
    echo "❌ ERROR: No se pudo conectar a PostgreSQL después de $MAX_TRIES intentos"
    exit 1
  fi
  echo "⏳ PostgreSQL no está listo - esperando..."
  sleep 2
done

echo "✅ PostgreSQL está listo"

# ===============================
# Migraciones
# ===============================
echo "📦 Aplicando migraciones..."
python manage.py migrate --noinput

# ===============================
# Superusuario + grupo admin
# ===============================
echo "👤 Verificando superusuario y grupo admin..."

python manage.py shell << 'END'
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import os

User = get_user_model()

username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")

# Grupo admin
admin_group, created = Group.objects.get_or_create(name="admin")
if created:
    print("✅ Grupo 'admin' creado.")
else:
    print("ℹ️  El grupo 'admin' ya existe.")

# Superusuario
if not User.objects.filter(username=username).exists():
    user = User.objects.create_superuser(
        username=username,
        password=password,
        email=email,
    )
    print(f"✅ Superusuario '{username}' creado.")
else:
    user = User.objects.get(username=username)
    print(f"ℹ️  El superusuario '{username}' ya existe.")

# Asociar grupo
if not user.groups.filter(name="admin").exists():
    user.groups.add(admin_group)
    print(f"✅ Usuario '{username}' agregado al grupo 'admin'.")
else:
    print(f"ℹ️  El usuario '{username}' ya pertenece al grupo 'admin'.")
END

# ===============================
# Arranque final
# ===============================
echo "🚀 Todo listo. Iniciando servidor..."
exec "$@"
