"""
Django settings for camerahub project.

Generated by 'django-admin startproject' using Django 2.1.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('CAMERAHUB_SECRET_KEY', 'OverrideMe!')

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv('CAMERAHUB_PROD') == 'true':
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_prometheus',
    'schema',
    'api',
    'djmoney',
    'django_tables2',
    'crispy_forms',
    'fullurl',
    'django_filters',
    'watson',
    'taggit',
    'django_social_share',
    'django_countries',
    'dal',
    'dal_select2',
    'bootstrap_datepicker_plus',
    'geoposition',
    'leaflet',
    'rest_framework',
    'drf_generators',
    'dbbackup',
    'health_check',
    'health_check.db',
    'colorfield',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
    'camerahub.middleware.DynamicSiteDomainMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'camerahub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_settings_export.settings_export',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'camerahub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# Configure databases by setting env vars CAMERAHUB_DB_*

DATABASES = {
    'default': {
        'ENGINE': os.getenv('CAMERAHUB_DB_ENGINE', 'django_prometheus.db.backends.sqlite3'),
        'NAME': os.getenv('CAMERAHUB_DB_NAME', os.path.join(BASE_DIR, 'db', 'db.sqlite3')),
        'USER': os.getenv('CAMERAHUB_DB_USER'),
        'PASSWORD': os.getenv('CAMERAHUB_DB_PASS'),
        'HOST': os.getenv('CAMERAHUB_DB_HOST'),
        'PORT': os.getenv('CAMERAHUB_DB_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = False
USE_TZ = True

DATE_INPUT_FORMATS = ['%Y-%m-%d', ]
DATETIME_INPUT_FORMATS = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M']
TIME_INPUT_FORMATS = ['%H:%M:%S', '%H:%M', ]

DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'Y-m-d H:i'
SHORT_DATE_FORMAT = 'Y-m-d'
SHORT_DATETIME_FORMAT = 'Y-m-d H:i'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# Where to put static files when they are collected
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Where to serve static files from
STATIC_URL = '/static/'

# Where to store uploaded assets
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Where to serve uploaded assets from
MEDIA_URL = '/media/'

# Add media to the list of static dirs
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'media/'),
]

DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"

LOGIN_REDIRECT_URL = 'schema:index'
LOGOUT_REDIRECT_URL = 'schema:index'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Email support
DEFAULT_FROM_EMAIL = os.getenv('CAMERAHUB_FROM_EMAIL', "noreply@camerahub.info")
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_BACKEND = os.getenv('CAMERAHUB_EMAIL_BACKEND', 'django.core.mail.backends.filebased.EmailBackend')

if EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
    EMAIL_USE_TLS = os.getenv('CAMERAHUB_EMAIL_USE_TLS')
    EMAIL_USE_SSL = os.getenv('CAMERAHUB_EMAIL_USE_SSL')
    EMAIL_HOST = os.getenv('CAMERAHUB_EMAIL_HOST')
    EMAIL_HOST_USER = os.getenv('CAMERAHUB_EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('CAMERAHUB_EMAIL_HOST_PASSWORD')
    EMAIL_PORT = os.getenv('CAMERAHUB_EMAIL_PORT')
elif EMAIL_BACKEND == 'django.core.mail.backends.filebased.EmailBackend':
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window
REGISTRATION_OPEN = True  # allow sign-ups

# Required for django.contrib.sites
DEFAULT_SITE_ID = 1
SITE_ID = 1

#AUTH_USER_MODEL = 'schema.User'

# Emit logs of WARNING and above to stderr
# for both production and debug mode
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console2': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console2'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'WARNING'),
        },
    },
}

TAGGIT_CASE_INSENSITIVE = True

# Use OpenStreetMap instead of Google for form widget
GEOPOSITION_BACKEND = 'leaflet'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': os.path.join(BASE_DIR, "backup")}
DBBACKUP_CONNECTORS = {
    'default': {
        'USER': os.getenv('CAMERAHUB_DB_USER'),
        'PASSWORD': os.getenv('CAMERAHUB_DB_PASS'),
        'HOST': os.getenv('CAMERAHUB_DB_HOST'),
        'CONNECTOR': 'dbbackup.db.postgresql.PgDumpBinaryConnector',
    }
}

# drf-generators
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25
}

# status URL
STATUS_URL = os.getenv('CAMERAHUB_STATUS_URL')

# django-settings-export
# These settings are exposed to template context
SETTINGS_EXPORT = [
    'STATUS_URL',
]

# Explicitly set the type of autofield to its current value
# In Django 3.2+ this will default to BigAutoField
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
