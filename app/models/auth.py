from uuid import uuid4
from werkzeug.security import generate_password_hash
import hashlib
import os
import sqlalchemy as sa
from flask import current_app

from app.models import db


class User(db.Model):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True)
    uid = sa.Column(sa.String(36),
                    unique=True,
                    index=True,
                    default=lambda: str(uuid4()))
    username = sa.Column(sa.String(64), unique=True, nullable=False)
    password = sa.Column(sa.String(128), nullable=False)
    email = sa.Column(sa.String(256), unique=True, nullable=False)
    avatar = sa.Column(sa.String(256), default="avatar/default.png")
    stuff = sa.Column(sa.Boolean, default=False)
    superuser = sa.Column(sa.Boolean, default=False)
    active = sa.Column(sa.Boolean, default=True)

    def __init__(self, username, email, **kwargs) -> None:
        self.username = username
        self.email = email
        self.stuff = kwargs.get("stuff", False)
        self.superuser = kwargs.get("superuser", False)

    def __repr__(self) -> str:
        return "<User {}>".format(self.username)

    @property
    def is_admin(self) -> bool:
        return self.superuser

    @property
    def is_stuff(self) -> bool:
        return self.stuff

    def set_password(self, password) -> None:
        self.password = generate_password_hash(password)

    def get_roles(self) -> str:
        if self.is_admin:
            return "admin"
        if self.is_stuff:
            return "stuff"
        return "ordinary"

    @staticmethod
    def allow_avatar_file(filename) -> bool:
        return "." in filename and \
            filename.rsplit('.', 1)[1].lower() in ["png", "jpg", "jpeg"]

    def avatar_upload_to(self, filename: str) -> str:
        upload_dir = "avatar/{}".format(self.username)
        try:
            os.mkdir(
                os.path.join(current_app.config["UPLOAD_FOLDER"], upload_dir))
        except OSError:
            pass
        ext = filename.rsplit(".", 1)[1].lower() if "." in filename else None
        return "{}/{}.{}".format(upload_dir, uuid4().hex, ext)

    def delete_avatar_file(self) -> None:
        if self.avatar == "avatar/default.png":
            return
        try:
            avatar_file = os.path.join(current_app.config["UPLOAD_FOLDER"],
                                       self.avatar)
            os.remove(avatar_file)
        except OSError:
            pass


class Token(db.Model):
    __tablename__ = "tokens"
    id = sa.Column(sa.Integer, primary_key=True)
    user = sa.Column(sa.Integer, sa.ForeignKey("users.uid"))
    value = sa.Column(sa.String(40),
                      unique=True,
                      index=True,
                      default=lambda: hashlib.sha1(os.urandom(24)).hexdigest())

    def __init__(self, user):
        self.user = user
