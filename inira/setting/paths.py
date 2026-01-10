import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "output")
PLANTILLAS_DATA_ROOT = os.path.join(BASE_DIR, "app", "Core", "data")
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"