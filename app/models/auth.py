from uuid import uuid4
import hashlib
import os
from werkzeug.security import generate_password_hash
import sqlalchemy as sa

from app.models import db


class User(db.Model):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True)
    uid = sa.Column(sa.String(36), unique=True, index=True,
                    default=lambda: str(uuid4()))
    username = sa.Column(sa.String(64), unique=True, nullable=False)
    password = sa.Column(sa.String(128), nullable=False)
    email = sa.Column(sa.String(256), unique=True, nullable=False)
    stuff = sa.Column(sa.Boolean, default=False)
    superuser = sa.Column(sa.Boolean, default=False)
    active = sa.Column(sa.Boolean, default=True)

    def __init__(self, username, password, email, stuff=False, superuser=False) -> None:
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.stuff = stuff
        self.superuser = superuser

    def __repr__(self) -> str:
        return "<User {}>".format(self.username)

    @property
    def is_superuser(self) -> bool:
        return self.superuser

    @property
    def is_admin(self) -> bool:
        return self.superuser

    @property
    def is_stuff(self) -> bool:
        return self.superuser

    @property
    def is_active(self) -> bool:
        return self.is_active

    def get_roles(self) -> str:
        if self.is_admin:
            return "admin"
        if self.is_stuff:
            return "stuff"
        return "ordinary"


class Token(db.Model):
    __tablename__ = "tokens"
    id = sa.Column(sa.Integer, primary_key=True)
    user = sa.Column(sa.Integer, sa.ForeignKey("users.uid"))
    value = sa.Column(sa.String(40), unique=True, index=True,
                      default=hashlib.sha1(os.urandom(24)).hexdigest)

    def __init__(self, user):
        self.user = user
