DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "drf_yasg",
    "django_json_widget",
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    "corsheaders",
]

LOCAL_APPS = [

 
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
