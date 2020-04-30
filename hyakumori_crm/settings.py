"""
Django settings for hyakumori_crm project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import urllib.parse
from datetime import timedelta
from distutils.util import strtobool

import dj_database_url
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "change this please")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.getenv("DEBUG", "no"))

ALLOWED_HOSTS = ["localhost"]
ALLOWED_HOSTS += os.getenv("ALLOWED_HOSTS", "").split(",")

# Application definition
STATIC_ROOT = os.path.join(
    BASE_DIR, os.getenv("STATIC_DIR", "hyakumori_crm/static/hyakumori_crm/dist")
)

if os.getenv("STATIC_DIR") == "":
    STATIC_ROOT = None

static_app = []
if not STATIC_ROOT and DEBUG:
    static_app = ["hyakumori_crm.static"]

orjson_experiment = []
if DEBUG:
    orjson_experiment = ["hyakumori_crm.core.response"]

INSTALLED_APPS = [
    *orjson_experiment,
    "whitenoise.runserver_nostatic",
    *static_app,  # this need high priority due to some override commands
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "ariadne.contrib.django",
    # ─── THIRD PARTIES APP ──────────────────────────────────────────────────────────
    "django_extensions",
    "rest_framework",
    "behaviors.apps.BehaviorsConfig",
    "guardian",
    "django_filters",
    # ─── HYAKUMORI APPS ─────────────────────────────────────────────────────────────
    "hyakumori_crm.crm",
    "hyakumori_crm.users",
    "hyakumori_crm.customer",
    "hyakumori_crm.forest",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hyakumori_crm.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [STATIC_ROOT] if STATIC_ROOT else [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "hyakumori_crm.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": dict(
        **dj_database_url.parse(
            urllib.parse.quote(os.environ.get("DATABASE_URL"), ":/@")
        )
    )
}

# Specify test database name
DATABASES["default"]["TEST"] = dict(
    NAME=os.getenv("DB_TEST_NAME", DATABASES["default"]["NAME"] + "__test")
)

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "ja"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_URL = "/"

AUTH_USER_MODEL = "users.User"

LANGUAGES = [("ja", _("Japan"))]

LOCALE_PATHS = [os.path.join(BASE_DIR, "hyakumori_crm", "locale")]

CORS_ORIGIN_WHITELIST = ["http://localhost:8080", "http://127.0.0.1:8080"]
CORS_ORIGIN_WHITELIST += os.getenv("CORS_ORIGIN_WHITELIST", "").split(",")

# ---------------------------------------------------------------------------- #
#                                    CACHES                                    #
# ---------------------------------------------------------------------------- #
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "hyakumori_crm_caches",
    }
}

# ---------------------------------------------------------------------------- #
#                                    AUTH                                      #
# ---------------------------------------------------------------------------- #

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)

# Djoser
DJOSER = {
    "PASSWORD_RESET_CONFIRM_URL": "auth/reset-password/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "auth/reset-username/{uid}/{token}",
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "ACTIVATION_URL": "auth/activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "USER_CREATE_PASSWORD_RETYPE": False,
    "SERIALIZERS": {
        "activation": "hyakumori_crm.users.serializers.ActivationSerializer",
        "user": "hyakumori_crm.users.serializers.UserSerializer",
        "current_user": "hyakumori_crm.users.serializers.UserSerializer",
        "user_create": "hyakumori_crm.users.serializers.UserCreateSerializer",
    },
    "EMAIL": {
        "activation": "hyakumori_crm.users.emails.ActivationEmail",
    },
    "PERMISSIONS": {"user_list": ["rest_framework.permissions.IsAdminUser"]},
    "LOGIN_FIELD": "email",
    "HIDE_USERS": True,
}

# Simple JWT
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT", "Bearer"),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "VERIFYING_KEY": None,
    "AUDIENCE": "Hyakumori",
    "ISSUER": "Hyakumori",
}

# Django Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "hyakumori_crm.crm.restful.paginations.StandardPagination",
    "PAGE_SIZE": int(os.getenv("DJANGO_PAGINATION_LIMIT", 10)),
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "60/minute", "user": "300/minute"},
}

DRF_TYPED_VIEWS = {"schema_packages": ["pydantic"]}

# Email
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "hyakumori_crm.mailing.backends.hyakumori.EmailBackend"
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "0.0.0.0")
EMAIL_PORT = os.getenv("EMAIL_PORT", 1025)
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
# EMAIL_USE_TLS = strtobool(os.getenv("EMAIL_USE_TLS", "no"))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "WARNING",
            "propagate": False,
        },
    },
}

# Under proxy, need this configuration so that restframework can apply https instead of http
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
