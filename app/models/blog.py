import sqlalchemy as sa
from datetime import datetime

from app.utils import slugify
from app.models import db
from app.models.auth import User


class Category(db.Model):
    __tablename__ = "categories"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(64), unique=True)
    slug = sa.Column(sa.String(128), unique=True, index=True)

    def __init__(self, name) -> None:
        self.name = name
        self.update_slug()

    def update_slug(self) -> None:
        self.slug = slugify(self.name)


class Article(db.Model):
    __tablename__ = "articles"
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(100), unique=True)
    abstract = sa.Column(sa.Text)
    content = sa.Column(sa.Text)
    author = sa.Column(sa.String(36), sa.ForeignKey(User.uid))
    category = sa.Column(sa.String(128), sa.ForeignKey(
        Category.slug), nullable=True)
    slug = sa.Column(sa.String(256), unique=True, index=True)
    views = sa.Column(sa.Integer, default=0)
    created = sa.Column(sa.DateTime, default=datetime.now)
    updated = sa.Column(sa.DateTime, default=datetime.now,
                        onupdate=datetime.now)

    def __init__(self, title, abstract, content, **kwargs) -> None:
        self.title = title
        self.abstract = abstract
        self.content = content
        self.category = kwargs.get("category", None)
        self.author = kwargs.get("author", None)
        self.update_slug()

    def update_slug(self) -> None:
        self.slug = slugify(self.title)


class About(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    article = sa.Column(sa.String(100), sa.ForeignKey(Article.slug))

    def __init__(self, article) -> None:
        self.id = 0
        self.article = article
