"""Personal Config Example"""

from pathlib import Path

ENV = "dev"

BASE_DIR = Path(__file__).resolve().parent

base_settings = {
    'SECRET_KEY':  'examplesecretkey',
}

settings = {
    # production env settings
    "prod": {
        "DEBUG": False,
        "ALLOWED_HOSTS": ['127.0.0.1'],
        "CORS_ORIGIN_ALLOW_ALL": False,
        "CORS_ORIGIN_WHITELIST": [],

        "DATABASES": {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'blog',
                'USER': 'xxx',
                'PASSWORD': 'xxx',
                'HOST': 'localhost',
                'PORT': '3306',
            }
        },

        "CACHES": {
            'default': {
                'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
                'LOCATION': '127.0.0.1:11211',
            }
        },

        'LOGS_DIR': '/path/to/log/dir',
        'DJANGO_LOG_LEVEL': 'WARNING',
    },

    # develop env settings
    "dev": {
        "DEBUG": True,
        "ALLOWED_HOSTS": ['*'],
        "CORS_ORIGIN_ALLOW_ALL": True,

        "DATABASES": {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        },

        "CACHES": {
            'default': {
                'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            }
        },
    },
}

for setting in settings.values():
    setting.update(base_settings)
