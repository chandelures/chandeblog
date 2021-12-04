from sqlalchemy import or_
from flask import Blueprint, current_app, request
from flask_restful import Api, Resource

from app.utils.auth import verify_password, token_auth
from app.models import db
from app.models.auth import User, Token

bp = Blueprint("auth", __name__, url_prefix="/auth")
api = Api(bp)


class TokenLogin(Resource):
    def post(self) -> dict:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if not username:
            return {"err": "username is required"}, 400
        if not password:
            return {"err": "password is required"}, 400
        if verify_password(username, password):
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
        else:
            return {"err": "login failed"}, 400


class TokenLogout(Resource):
    decorator = [token_auth.login_required]

    def post(self) -> dict:
        pass


class Register(Resource):
    def post(self) -> dict:
        pass


class Profile(Resource):
    def get(self) -> dict:
        pass

    def put(self) -> dict:
        pass

    def delete(self) -> dict:
        pass


api.add_resource(TokenLogin, "/token/login")
api.add_resource(TokenLogout, "/token/logout")
api.add_resource(Register, "/register")
