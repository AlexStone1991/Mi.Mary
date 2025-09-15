from django.urls import reverse_lazy
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG_MODE", "True") == "True"

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '5.129.251.229',  # Ваш IP сервера
    'mi-mary.ru'  # Если есть домен
]

CSRF_TRUSTED_ORIGINS = [
    'http://5.129.251.229',
    'https://5.129.251.229',
    'http://mi-mary.ru',
    'https://mi-mary.ru'
]





# Application definition

INSTALLED_APPS = [
    # "jazzmin",
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_extensions",
    'debug_toolbar',
    "core",
    "users",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'mi_mary.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "core.context_processors.menu_items"
            ],
        },
    },
]

WSGI_APPLICATION = 'mi_mary.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'Mi_Mary_Base.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True



STATIC_URL = 'static/'
STATICFILES_DIRS  = [BASE_DIR / 'static']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = ['127.0.0.1']

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

MISTRAL_MODERATIONS_GRADES = {
    "hate_and_discrimination": 0.1,  # ненависть и дискриминация
    "sexual": 0.1,  # сексуальный
    "violence_and_threats": 0.1,  # насилие и угрозы
    "dangerous_and_criminal_content": 0.1,  # опасный и криминальный контент
    "selfharm": 0.1,  # самоповреждение
    "health": 0.1,  # здоровье
    "financial": 0.1,  # финансовый
    "law": 0.1,  # закон
    "pii": 0.1,  # личная информация
}

TELEGRAM_BOT_API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")
TELEGRAM_USER_ID_2 = os.getenv("TELEGRAM_USER_ID_2")

LOGIN_URL = reverse_lazy("login")
LOGIN_REDIRECT_URL = reverse_lazy("landing")
LOGOUT_REDIRECT_URL = reverse_lazy("landing")

# Новая модель пользователя users.models.CustomUser
AUTH_USER_MODEL = "users.CustomUser"

# Восстановление пароля в консоль
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_ID = 1

# Письма будут уходить smtp сервер
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.mail.ru"
EMAIL_PORT = 465  # Используем SSL
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False  # Отключаем TLS при использовании SSL
EMAIL_HOST_USER = os.getenv("EMAIL")  # Полный email-адрес
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # Пароль приложения
DEFAULT_FROM_EMAIL = os.getenv("EMAIL")
SERVER_EMAIL = os.getenv("EMAIL")

# Настройки логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}