"""Personal Config Example"""

ENV = "dev"

base_settings = {
    'SECRET_KEY':  'examplesecretkey',
}

settings = {
    # production env settings
    "prod": {
        "DEBUG": False,
        "ALLOWED_HOSTS": ['127.0.0.1'],
        "CORS_ORIGIN_ALLOW_ALL": False,
    },

    # develop env settings
    "dev": {
        "DEBUG": True,
        "ALLOWED_HOSTS": ['*'],
        "CORS_ORIGIN_ALLOW_ALL": True,
    },
}

for setting in settings.values():
    setting.update(base_settings)
