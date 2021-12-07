from sqlalchemy import or_
from flask import Blueprint, current_app, request
from flask_restful import Api, Resource

from app.utils.auth import check_password, verify_password
from app.utils.auth import token_auth
from app.models import db
from app.models.auth import User, Token

bp = Blueprint("auth", __name__, url_prefix="/auth")
api = Api(bp)


class TokenLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return {"detail": "username and password is required"}, 400
        if not verify_password(username, password):
            return {"detail": "login failed"}, 400
        with current_app.app_context():
            user = User.query.filter(
                or_(User.username == username, User.email == username)).first()
            token = Token.query.filter_by(user=user.uid).first()
            if token:
                return {"token": token.value}
            token = Token(user.uid)
            db.session.add(token)
            db.session.commit()
            return {"token": token.value}


class TokenLogout(Resource):
    decorators = [token_auth.login_required]

    def post(self):
        user = token_auth.current_user()
        with current_app.app_context():
            token = Token.query.filter_by(user=user.uid).first()
            db.session.delete(token)
            db.session.commit()
        return {"detail": "success"}


class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        if not username or not password or not email:
            return {"detail": "username, password, email is required"}, 400
        if not check_password(password):
            return {"detail": "invalid password"}, 400
        with current_app.app_context():
            user = User(username, password, email)
            db.session.add(user)
            db.session.commit()
        return {"detail": "success"}


class ProfileList(Resource):
    decorators = [token_auth.login_required]

    def get(self):
        pass


class ProfileDetail(Resource):
    decorators = [token_auth.login_required]

    def get(self):
        user = token_auth.current_user()
        return {
            "uid": user.uid,
            "username": user.username,
            "isAdmin": user.is_admin,
        }

    def put(self):
        user = token_auth.current_user()
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        with current_app.app_context():
            if username:
                user.username = username
            if password:
                user.password = password
            if email:
                user.email = email
            db.session.commit()
        return {"detail": "success"}

    def delete(self):
        user = token_auth.current_user()
        with current_app.app_context():
            user.active = False
            db.session.commit()
        return {"detail": "success"}


api.add_resource(TokenLogin, "/token/login")
api.add_resource(TokenLogout, "/token/logout")
api.add_resource(Register, "/register")
api.add_resource(ProfileDetail, "/users/profile")
api.add_resource(ProfileList, "/users")
