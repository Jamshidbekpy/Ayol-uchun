from datetime import timedelta
import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv
import environ

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = ["*"]


# READING ENV
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))


DJANGO_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "apps.accounts",
    "apps.courses",
    "apps.news",
    "apps.common",
]

EXTERNAL_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "drf_yasg",
    "rosetta",
    "modeltranslation",
    "query_counter",
]


INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + EXTERNAL_APPS

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        # "apps.text_services.filters.MultiSymbolSearchFilter",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}


MIDDLEWARE = [
    "query_counter.middleware.DjangoQueryCounterMiddleware",  # query-counter
    "django.middleware.locale.LocaleMiddleware",  # locale
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

QUERY_COUNTER = {
    "DQC_SLOWEST_COUNT": 5,
    "DQC_TABULATE_FMT": "pretty",
    "DQC_SLOW_THRESHOLD": 1,
    "DQC_INDENT_SQL": True,
    "DQC_PYGMENTS_STYLE": "tango",
    "DQC_PRINT_ALL_QUERIES": True,
    "DQC_DETECT_DUPLICATES": True,
    "DQC_DUPLICATE_COLOR": "red",
    "DQC_COUNT_QTY_MAP": {
        5: "green",
        10: "white",
        20: "yellow",
        30: "red",
    },
}

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
# ASGI_APPLICATION = 'core.asgi.application'


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "ATOMIC_REQUESTS": False,  # True
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tashkent"

LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
    ("uz", _("Uzbek")),
]

USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = (BASE_DIR / "locale",)


# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = (BASE_DIR / "staticfiles",)

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# CACHES
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"{REDIS_HOST}:{REDIS_PORT}",
        "KEY_PREFIX": "boilerplate",  # todo: you must change this with your project name or something else
    }
}


# CELERY CONFIGURATION
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}")
CELERY_RESULT_BACKEND = os.getenv(
    "CELERY_RESULT_BACKEND", f"redis://{REDIS_HOST}:{REDIS_PORT}"
)

CELERY_TIMEZONE = "Asia/Tashkent"

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60


# CYPHER CONFIGURATION
# AES
AES_KEY = os.getenv("AES_KEY", "")


# RECAPTCHA
# RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY")
# RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY")
AUTH_USER_MODEL = "accounts.User"


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = env.str("EMAIL_HOST", "localhost")
EMAIL_PORT = env.int("EMAIL_PORT", 1025)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", False)
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", "")


# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [(REDIS_HOST, REDIS_PORT)],
#         },
#     },
# }

ESKIZ_EMAIL = env.str("ESKIZ_EMAIL", "WlV5w@example.com")
ESKIZ_PASSWORD = env.str("ESKIZ_PASSWORD", "password")
ESKIZ_BASE_URL = env.str("ESKIZ_BASE_URL", "https://eskiz.uz")
