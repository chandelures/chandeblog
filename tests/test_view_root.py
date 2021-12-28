from flask import Flask
from flask.helpers import url_for


def test_root(client, app: Flask):
    assert client.get("/").status_code == 200


def test_build_media_path(client, app: Flask):
    with app.app_context():
        assert url_for("world.media",
                       path="avatar/default.png",
                       _external=False) == "/media/avatar/default.png"
