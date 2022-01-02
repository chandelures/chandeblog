from flask.app import Flask
from app.utils.auth import create_superuser


def init_app(app: Flask):
    app.cli.add_command(create_superuser)


def slugify(s: str) -> str:
    return s.replace(" ", "-")
