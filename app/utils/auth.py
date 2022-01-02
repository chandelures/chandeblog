from typing import Union, Tuple
import click
from werkzeug.security import check_password_hash
from sqlalchemy import or_
from flask import current_app
from flask.cli import with_appcontext
from flask_httpauth import HTTPTokenAuth

from app.models import db
from app.models.auth import User, Token

token_auth = HTTPTokenAuth()


@click.command("createsuperuser")
@click.option("--username", default="")
@click.option("--email", default="")
@click.option("--password", default="")
@with_appcontext
def create_superuser(username, email, password) -> None:
    if not username or not email or not password:
        click.echo("Failed.")
        return
    user = User(username, email, stuff=True, superuser=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo("Created.")


def check_password(password) -> bool:
    if len(password) < 6:
        return False
    return True


def verify_password(username, password) -> Union[User, None]:
    with current_app.app_context():
        user = User.query.filter(
            or_(User.username == username, User.email == username)).first()
        if not user:
            return
        if not user.active:
            return
        if check_password_hash(user.password, password):
            return user


@token_auth.verify_token
def verify_token(token) -> Union[User, None]:
    with current_app.app_context():
        token = Token.query.filter_by(value=token).first()
        if token:
            return User.query.filter_by(uid=token.user).first()


@token_auth.get_user_roles
def get_user_roles(user: User) -> str:
    return user.get_roles()


@token_auth.error_handler
def error_handler(status) -> Tuple[dict, int]:
    return {"detail": "Unauthorized Access"}, status
