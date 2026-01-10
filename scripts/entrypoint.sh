#!/bin/bash
set -e

echo "=== 🚀 Iniciando entrypoint (entorno:) ==="

echo "⌛ Esperando a que la base de datos esté disponible..."
sleep 5

echo "📦 Aplicando migraciones existentes..."
python manage.py migrate --noinput

echo "🎨 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

python manage.py shell << 'END'
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password, email=email)
    print(f"✅ Superusuario '{username}' creado.")
else:
    print(f"ℹ️ El superusuario '{username}' ya existe.")
END

echo "✅ Entrypoint completado. Iniciando aplicación..."
exec "$@"
