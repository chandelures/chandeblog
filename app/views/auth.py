from sqlalchemy import or_
from flask import Blueprint, request
from flask.helpers import url_for
from flask.views import MethodView

from webargs.flaskparser import parser

from app.utils.error import invalid_api_usage
from app.utils.args import pagination_args
from app.utils.auth import check_password, verify_password, token_auth
from app.models import db
from app.models.auth import User, Token

bp = Blueprint("auth", __name__, url_prefix="/auth")


class TokenLogin(MethodView):

    def post(self):
        data = request.get_json() or {}
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return invalid_api_usage("No username or password provided", 400)
        if not verify_password(username, password):
            return invalid_api_usage("Invalid username or password", 400)
        user = User.query.filter(
            or_(User.username == username, User.email == username)).first()
        token = Token.query.filter_by(user=user.uid).first()
        if token:
            return {"token": token.value}
        token = Token(user.uid)
        db.session.add(token)
        db.session.commit()
        return {"token": token.value}


class TokenLogout(MethodView):
    decorators = [token_auth.login_required]

    def post(self):
        user = token_auth.current_user()
        token = Token.query.filter_by(user=user.uid).first()
        db.session.delete(token)
        db.session.commit()
        return {"message": "success"}


class Register(MethodView):

    def post(self):
        data = request.get_json() or {}
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        if not username or not password or not email:
            return invalid_api_usage("No username, password, email provided",
                                     400)
        if not check_password(password):
            return invalid_api_usage("Invalid password", 400)
        user = User(username, email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return {"message": "success"}, 201


class ProfileList(MethodView):
    decorators = [token_auth.login_required(role=["admin", "stuff"])]

    @parser.use_args(pagination_args, location="query")
    def get(self, args):
        pagination = User.query.filter_by().paginate(
            page=args["page"],
            per_page=args["size"],
        )
        return {
            "count":
            pagination.total,
            "next":
            url_for("world.auth.profiles",
                    page=pagination.next_num,
                    _external=True) if pagination.has_next else None,
            "previous":
            url_for("world.auth.profiles",
                    page=pagination.prev_num,
                    _external=True) if pagination.has_prev else None,
            "results": [{
                "uid": item.uid,
                "username": item.username,
                "email": item.email,
            } for item in pagination.items]
        }


class ProfileDetail(MethodView):
    decorators = [token_auth.login_required]

    def get(self):
        user = token_auth.current_user()
        item = User.query.filter_by(uid=user.uid).first()
        return {
            "uid": item.uid,
            "username": item.username,
            "email": item.email,
            "isAdmin": item.is_admin,
        }

    def put(self):
        user = token_auth.current_user()
        item = User.query.filter_by(uid=user.uid).first()
        data = request.get_json() or {}
        username = data.get("username")
        email = data.get("email")
        if not username or not email:
            return invalid_api_usage("No username or email provided", 400)

        attrs = dict(username=username, email=email)
        for name, value in attrs.items():
            setattr(item, name, value)
        db.session.commit()

        return {
            "uid": item.uid,
            "username": item.username,
            "email": item.email,
            "isAdmin": item.is_admin,
        }

    def delete(self):
        user = token_auth.current_user()
        item = User.query.filter_by(uid=user.uid).first()
        item.active = False
        db.session.commit()
        return {"message": "success"}


bp.add_url_rule("/token/login",
                view_func=TokenLogin.as_view("token-login"),
                endpoint="token-login")
bp.add_url_rule("/token/logout",
                view_func=TokenLogout.as_view("token-logout"),
                endpoint="token-logout")
bp.add_url_rule("/register",
                view_func=Register.as_view("register"),
                endpoint="register")
bp.add_url_rule("/users",
                view_func=ProfileList.as_view("profiles"),
                endpoint="profiles")
bp.add_url_rule("/users/profile",
                view_func=ProfileDetail.as_view("profile-detail"),
                endpoint="profile-detail")
