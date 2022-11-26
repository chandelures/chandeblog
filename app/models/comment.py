from datetime import datetime
import sqlalchemy as sa

from app.models import db
from app.models.auth import User
from app.models.blog import Post


class Comment(db.Model):
    __tablename__ = "comments"
    uid = sa.Column(sa.String(36), primary_key=True)
    post = sa.Column(sa.String(128), sa.ForeignKey(Post.slug))
    user = sa.Column(sa.String(36), sa.ForeignKey(User.uid))
    content = sa.Column(sa.Text)
    created = sa.Column(sa.DateTime, default=datetime.now)
    updated = sa.Column(sa.DateTime,
                        default=datetime.now,
                        onupdate=datetime.now)
    parent = sa.Column(sa.String(36),
                       sa.ForeignKey("comments.uid"),
                       nullable=True)
    reply = sa.Column(sa.String(36), sa.ForeignKey(User.uid), nullable=True)

    def __init__(self, article, content, user, **kwags) -> None:
        self.article = article
        self.content = content
        self.user = user
        for name, value in kwags.items():
            setattr(self, name, value)

    @property
    def is_root(self):
        return self.parent is None
