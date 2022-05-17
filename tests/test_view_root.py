from flask import Flask
from flask.helpers import url_for


def test_root(client, app: Flask) -> None:
    url = "/"
    res = client.get(url)
    assert res.is_json
    assert res.status_code == 200


def test_build_media_path(app: Flask) -> None:
    with app.app_context():
        assert url_for("world.media",
                       path="avatar/default.png",
                       _external=False) == "/media/avatar/default.png"
