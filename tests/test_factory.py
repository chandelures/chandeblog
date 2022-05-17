from flask import Flask

from app import create_app
from app import wsgi


def test_config() -> None:
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_wsgi() -> None:
    assert isinstance(wsgi.app, Flask)
