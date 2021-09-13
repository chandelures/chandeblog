"""
Django local_settings for chandeblog project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/local_settings/

For the full list of local_settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/local_settings/
"""

from pathlib import Path

try:
    from config import local_settings, ENV
    for setting in local_settings.values():
        setting.update(local_settings['base'])
    local_settings = local_settings.get(ENV)

except ImportError:
    ENV = 'dev'
    local_settings = {}
    pass


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development local_settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = local_settings.get('SECRET_KEY', '*')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = local_settings.get('DEBUG', False)

ALLOWED_HOSTS = local_settings.get('ALLOWED_HOSTS', ['localhost'])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',

    'blog',
    'userprofile',
    'comment',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chandeblog.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'chandeblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/local_settings/#databases

DATABASES = local_settings.get('DATABASES', {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
})


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/local_settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = Path(BASE_DIR, 'static')

# Authentication Backends Config
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'userprofile.backends.EmailBackend',
)

# Other

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# RSS config
RSS_LINK_HOST = local_settings.get('RSS_LINK_HOST', '/')

RSS_TITLE = local_settings.get('RSS_TITLE', 'chandeblog')

RSS_DISCRIPTION = local_settings.get('RSS_DISCRIPTION', 'chandeblog 全部文章')

# Media config
MEDIA_URL = '/media/'

MEDIA_ROOT = Path.joinpath(BASE_DIR, 'media')

# CORS config
CORS_ORIGIN_ALLOW_ALL = local_settings.get("CORS_ORIGIN_ALLOW_ALL", False)

CORS_ORIGIN_WHITELIST = local_settings.get("CORS_ORIGIN_WHITELIST", [])

# Rest Framework config

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': 'blog.paginations.PageNumberPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

if ENV == "prod":
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
    )
elif ENV == "dev":
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

# Logging config
DJANGO_LOG_LEVEL = local_settings.get('DJANGO_LOG_LEVEL', 'INFO')

if ENV == 'prod':
    LOGS_DIR = local_settings.get('LOGS_DIR')
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '{levelname} {asctime} {message}',
                'style': '{',
            }
        },
        'handlers': {
            'file': {
                'level': DJANGO_LOG_LEVEL,
                'class': 'logging.FileHandler',
                'formatter': 'default',
                'filename': Path(LOGS_DIR).joinpath('django.log'),
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': True,
            }
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': DJANGO_LOG_LEVEL,
                'propagate': True,
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': False,
            },
        },
    }
elif ENV == 'dev':
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': DJANGO_LOG_LEVEL,
                'propagate': True,
            },
        },
    }

# Email config
EMAIL_HOST = local_settings.get('EMAIL_HOST', 'localhost')

EMAIL_PORT = local_settings.get('EMAIL_PORT', 25)

EMAIL_HOST_USER = local_settings.get('EMAIL_HOST_USER', '')

EMAIL_HOST_PASSWORD = local_settings.get('EMAIL_HOST_PASSWORD', '')

EMAIL_USE_TLS = local_settings.get('EMAIL_USE_TLS', False)

EMAIL_USE_SSL = local_settings.get('EMAIL_USE_SSL', False)

EMAIL_FROM = EMAIL_HOST_USER

# Admin config
ADMINS = local_settings.get('ADMINS', [])

SERVER_EMAIL = EMAIL_HOST_USER
