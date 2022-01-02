import pytest

import tempfile
import shutil
from flask import json
from flask.app import Flask

from app import create_app
from app.models import db
from app.models.auth import User


@pytest.fixture
def app():
    db_dir = tempfile.mkdtemp()
    media_dir = tempfile.mkdtemp()

    app = create_app({
        "TESTTING":
        True,
        "SERVER_NAME":
        "localhost.localdomain",
        "SQLALCHEMY_DATABASE_URI":
        "sqlite:////{}/db.sqlite".format(db_dir),
        "UPLOAD_FOLDER":
        media_dir,
    })

    with app.app_context():
        db.create_all()
        user = User("admin", "admin@admin.org", stuff=True, superuser=True)
        user.set_password("admin")
        db.session.add(user)
        db.session.commit()

    yield app

    shutil.rmtree(db_dir)
    shutil.rmtree(media_dir)


@pytest.fixture
def client(app: Flask):
    return app.test_client()


@pytest.fixture
def user_client(app: Flask):
    client = app.test_client()
    user = User("temp", "temp@temp.org")
    user.set_password("temppsw")
    with app.app_context():
        db.session.add(user)
        db.session.commit()
    res = client.post("/auth/token/login",
                      json={
                          "username": "temp",
                          "password": "temppsw",
                      })
    token = json.loads(res.data).get("token")
    client.environ_base["HTTP_AUTHORIZATION"] = "Bearer {}".format(token)
    return client


@pytest.fixture
def stuff_client(app: Flask):
    client = app.test_client()
    user = User("stuff", "stuff@stuff.org", stuff=True)
    user.set_password("stuffpsw")
    with app.app_context():
        db.session.add(user)
        db.session.commit()
    res = client.post("/auth/token/login",
                      json={
                          "username": "stuff",
                          "password": "stuffpsw",
                      })
    token = json.loads(res.data).get("token")
    client.environ_base["HTTP_AUTHORIZATION"] = "Bearer {}".format(token)
    return client
