import pytest

from flask import Flask
from flask.testing import FlaskClient

from app.utils import slugify
from app.models import db
from app.models.blog import Article
from app.models.auth import User


def create_articles(app: Flask) -> None:
    article_titles = ["test title " + str(i) for i in range(10)]
    with app.app_context():
        for title in article_titles:
            admin = User.query.filter_by(username="admin").first()
            article = Article(
                title,
                "test abstarct",
                "test content",
                author=admin.uid,
            )
            db.session.add(article)
            db.session.commit()


def create_article(app: Flask) -> Article:
    with app.app_context():
        admin = User.query.filter_by(username="admin").first()
        article = Article("test title",
                          "test abstract",
                          "test content",
                          author=admin.uid)
        db.session.add(article)
        db.session.commit()
        article = Article.query.filter_by(title="test title").first()
    return article


@pytest.mark.parametrize(
    ("title", "abstract", "content", "status_code"),
    (("", "", "", 400), ("test title", "", "", 400),
     ("test title", "test abstract", "", 400),
     ("test title", "test abstract", "test content", 201)))
def test_create_article(client: FlaskClient, user_client: FlaskClient,
                        stuff_client: FlaskClient, app: Flask, title: str,
                        abstract: str, content: str, status_code: int) -> None:
    url = "/articles"
    data = {
        "title": title,
        "abstract": abstract,
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
        article = Article.query.filter_by(title=title).first()
    assert article
    assert article.slug == slugify(article.title)
    assert article.abstract == abstract
    assert article.content == content
    assert article.author


def test_get_article_list(client: FlaskClient, app: Flask) -> None:
    url = "/articles"
    create_articles(app)
    res = client.get(url)
    assert res.is_json
    assert res.status_code == 200


def test_get_article_detail(client: FlaskClient, app: Flask) -> None:
    url = "/articles/{}"
    article = create_article(app)
    res = client.get(url.format("not exists"))
    assert res.is_json
    assert res.status_code == 404
    res = client.get(url.format(article.slug))
    assert res.is_json
    assert res.status_code == 200


@pytest.mark.parametrize(("data"), (({
    "title": "other title",
    "abstract": "other abstract",
    "content": "other content",
}), ({})))
def test_update_article_detail(client: FlaskClient, user_client: FlaskClient,
                               stuff_client: FlaskClient, app: Flask,
                               data: dict) -> None:
    url = "/articles/{}"
    article = create_article(app)
    res = client.put(url.format(article.slug), json=data)
    assert res.is_json
    assert res.status_code == 401
    res = user_client.put(url.format(article.slug), json=data)
    assert res.is_json
    assert res.status_code == 403
    res = stuff_client.put(url.format(article.slug), json=data)
    assert res.is_json
    assert res.status_code == 200

    with app.app_context():
        article = Article.query.filter_by(title=data.get("title")).first()

    update_fields = ["title", "abstract", "content"]
    for field in update_fields:
        if field in data:
            assert getattr(article, field) == data.get(field)
            assert article.slug == slugify(article.title)


def test_delete_article_detail(client: FlaskClient, user_client: FlaskClient,
                               stuff_client: FlaskClient, app: Flask) -> None:
    url = "/articles/{}"
    article = create_article(app)
    res = client.delete(url.format(article.slug))
    assert res.is_json
    assert res.status_code == 401
    res = user_client.delete(url.format(article.slug))
    assert res.is_json
    assert res.status_code == 403
    res = stuff_client.delete(url.format(article.slug))
    assert res.is_json
    assert res.status_code == 200

    with app.app_context():
        assert not Article.query.filter_by(slug=article.slug).first()

    res = stuff_client.delete(url.format(article.slug))
    assert res.status_code == 204
