# ChandeBlog

This is a back end project for [chandeblog](https://blog.chandelure.com/) based on django and django rest framework.
The front end blog project is https://github.com/chandelures/chandeblog-frontend.git.

## Credits

- [Django](https://github.com/django/django)
- [Django Rest Framework](https://github.com/encode/django-rest-framework)

## Start Up Server

First, install dependencies

```shell
(env) $ pip install requirements.txt
```

Copy exmaple config

```shell
(env) $ cp config.example.py config.py
```

Run django project in development environment

```shell
(env) $ python manage.py runserver
```

Or in production enviroment

```shell
(env) $ gunicorn chandeblog.wsgi:application
```

## Config

- ENV: 'prod' || 'dev'

  Set the environment where you want to run porject.

- local_settings: {"base": {}, "prod": {}, "dev": {}}

  Set some basic settings such as SECRET_KEY, email settings used in both prod and dev environment. And there is the possibility that some settings are different in prod and dev enviroment.

Example:

```python
ENV = "dev"

BASE_DIR = Path(__file__).resolve().parent

local_settings = {
    "base": {
        'SECRET_KEY':  'examplesecretkey',

        'EMAIL_HOST': 'smtp.xxx.com',
        'EMAIL_PORT': 25,
        'EMAIL_HOST_USER': 'xxx@xxx.com',
        'EMAIL_HOST_PASSWORD': 'xxxxxxx',
        'EMAIL_USE_SSL': False,

        'ADMINS': [('xxx', 'xxx@xxx.com')],
    },

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
    },
}
```

## Deploy

There is a automatic script based on fabric to deloy this project at anywhere. You can update the fabfile in subdirectory named scripts to satisfy your requirements.

Install fabric

```shell
(env) $ pip install fabric
```

Run fabfile

```shell
(env) $ fab -r scripts
```

## License

[MIT License](https://raw.githubusercontent.com/chandelures/chandeblog/dev/LICENSE)
