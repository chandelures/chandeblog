import sqlalchemy as sa
from datetime import datetime

from app.utils import slugify
from app.models import db
from app.models.auth import User


class Post(db.Model):
    __tablename__ = "posts"
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(100), unique=True)
    description = sa.Column(sa.Text)
    content = sa.Column(sa.Text)
    author = sa.Column(sa.String(36), sa.ForeignKey(User.uid))
    slug = sa.Column(sa.String(128), unique=True, index=True)
    views = sa.Column(sa.Integer, default=0)
    created = sa.Column(sa.DateTime, default=datetime.now)
    updated = sa.Column(sa.DateTime,
                        default=datetime.now,
                        onupdate=datetime.now)

    def __init__(self, title, description, content, **kwargs) -> None:
        self.title = title
        self.description = description
        self.content = content
        for name, value in kwargs.items():
            if value:
                setattr(self, name, value)
        self.update_slug()

    def update_slug(self) -> None:
        self.slug = slugify(self.title)
