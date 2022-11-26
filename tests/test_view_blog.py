import pytest

from flask import Flask
from flask.testing import FlaskClient

from app.utils import slugify
from app.models import db
from app.models.blog import Post


def create_posts(app: Flask) -> None:
    post_titles = ["test title " + str(i) for i in range(10)]
    with app.app_context():
        for title in post_titles:
            post = Post(
                title,
                "test abstarct",
                "test content",
            )
            db.session.add(post)
            db.session.commit()


def create_post(app: Flask) -> Post:
    with app.app_context():
        post = Post(
            "test title",
            "test description",
            "test content",
        )
        db.session.add(post)
        db.session.commit()
        post = Post.query.filter_by(title="test title").first()
    return post


@pytest.mark.parametrize(
    ("title", "description", "content", "status_code"),
    (("", "", "", 400), ("test title", "", "", 400),
     ("test title", "test description", "", 400),
     ("test title", "test description", "test content", 201)))
def test_create_post(client: FlaskClient, user_client: FlaskClient,
                     stuff_client: FlaskClient, app: Flask, title: str,
                     description: str, content: str, status_code: int) -> None:
    url = "/posts"
    data = {
        "title": title,
        "description": description,
        "content": content,
    }

    res = client.post(url, json=data)
    assert res.is_json
    assert res.status_code == 401
    res = user_client.post(url, json=data)
    assert res.is_json
    assert res.status_code == 403
    res = stuff_client.post(url, json=data)
    assert res.is_json
    assert res.status_code == status_code

    if status_code == 400:
        return

    res = stuff_client.post(url, json=data)
    assert res.is_json
    assert res.status_code == 400

    with app.app_context():
        post = Post.query.filter_by(title=title).first()
    assert post
    assert post.slug == slugify(post.title)
    assert post.description == description
    assert post.content == content


def test_get_post_list(client: FlaskClient, app: Flask) -> None:
    url = "/posts"
    create_posts(app)
    res = client.get(url)
    assert res.is_json
    assert res.status_code == 200


def test_get_post_detail(client: FlaskClient, app: Flask) -> None:
    url = "/posts/{}"
    post = create_post(app)
    res = client.get(url.format("not exists"))
    assert res.is_json
    assert res.status_code == 404
    res = client.get(url.format(post.slug))
    assert res.is_json
    assert res.status_code == 200


@pytest.mark.parametrize(("data"), (({
    "title": "other title",
    "description": "other description",
    "content": "other content",
}), ({})))
def test_update_post_detail(client: FlaskClient, user_client: FlaskClient,
                            stuff_client: FlaskClient, app: Flask,
                            data: dict) -> None:
    url = "/posts/{}"
    post = create_post(app)
    res = client.put(url.format(post.slug), json=data)
    assert res.is_json
    assert res.status_code == 401
    res = user_client.put(url.format(post.slug), json=data)
    assert res.is_json
    assert res.status_code == 403
    res = stuff_client.put(url.format(post.slug), json=data)
    assert res.is_json
    assert res.status_code == 200

    with app.app_context():
        post = Post.query.filter_by(title=data.get("title")).first()

    update_fields = ["title", "description", "content"]
    for field in update_fields:
        if field in data:
            assert getattr(post, field) == data.get(field)
            assert post.slug == slugify(post.title)


def test_delete_post_detail(client: FlaskClient, user_client: FlaskClient,
                            stuff_client: FlaskClient, app: Flask) -> None:
    url = "/posts/{}"
    post = create_post(app)
    res = client.delete(url.format(post.slug))
    assert res.is_json
    assert res.status_code == 401
    res = user_client.delete(url.format(post.slug))
    assert res.is_json
    assert res.status_code == 403
    res = stuff_client.delete(url.format(post.slug))
    assert res.is_json
    assert res.status_code == 200

    with app.app_context():
        assert not Post.query.filter_by(slug=post.slug).first()

    res = stuff_client.delete(url.format(post.slug))
    assert res.status_code == 204
