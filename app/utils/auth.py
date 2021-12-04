from werkzeug.security import check_password_hash
from sqlalchemy import or_
from flask import current_app
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from app.models.auth import User, Token

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password) -> User or None:
    with current_app.app_context():
        user = User.query.filter(
            or_(User.username == username, User.email == username)).first()
        if not user:
            return
        if check_password_hash(user.password, password):
            return user


@token_auth.verify_token
def verify_token(token) -> User or None:
    with current_app.app_context():
        token = Token.query.filter_by(value=token).first()
        if token:
            return User.query.filter_by(uid=token.user).first()


@basic_auth.get_user_roles
@token_auth.get_user_roles
def get_user_roles(user: User) -> str:
    return user.get_roles()

@token_auth.error_handler
def error_handler(status) -> tuple:
    return {"detail": "Unauthorized Access"}, status
