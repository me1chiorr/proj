import os
from pathlib import Path

# 1) Определяем корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# 2) Загружаем переменные окружения из .env (должен лежать рядом с manage.py)
from dotenv import load_dotenv
load_dotenv(BASE_DIR / '.env')

# 3) Импортируем config для чтения из .env
from decouple import config

# 4) Ваши ключи для 2ГИС
DGIS_API_KEY   = config('DGIS_API_KEY')
DGIS_REGION_ID = config('DGIS_REGION_ID', default='29')

# ------------------------------------------------------------------------------
# Общие настройки Django
# ------------------------------------------------------------------------------

# Загружаем из .env
from decouple import config
SECRET_KEY = config('SECRET_KEY')
DEBUG      = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Локальное время для Алматы
TIME_ZONE = 'Asia/Almaty'
LOGIN_URL = '/accounts/login/'
# ------------------------------------------------------------------------------
# Приложения
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'django_filters',
    'main.apps.MainConfig',
    'rest_framework',    # DRF
    'drf_yasg',          # Swagger / OpenAPI
]

# ------------------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

# ------------------------------------------------------------------------------
# Шаблоны
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # указываем папку с вашими html
        'DIRS': [ BASE_DIR / 'main' / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# ------------------------------------------------------------------------------
# База данных
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------------------------------------------------------------------------------
# Валидаторы паролей
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ------------------------------------------------------------------------------
# Локализация
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ------------------------------------------------------------------------------
# Статика и медиа
# ------------------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR / 'main' / 'static' ]

# ------------------------------------------------------------------------------
# Переадресация после логина
# ------------------------------------------------------------------------------
LOGIN_REDIRECT_URL = '/reserve/'

# ------------------------------------------------------------------------------
# Почта (для регистрации)
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ------------------------------------------------------------------------------
# Остальные дефолты
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'restaurant-booking-cache',
    }
 }
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

YANDEX_MAPS_API_KEY = config("YANDEX_MAPS_API_KEY")

