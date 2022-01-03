import os
from sqlalchemy import or_
from werkzeug.utils import secure_filename
from flask import Blueprint, current_app, request
from flask.helpers import url_for
from flask_restful import Api, Resource
from app.utils.error import invalid_api_usage

from app.utils.pagination import pagination_parser, max_size
from app.utils.auth import check_password, verify_password, token_auth
from app.models import db
from app.models.auth import User, Token

bp = Blueprint("auth", __name__, url_prefix="/auth")
api = Api(bp)


class TokenLogin(Resource):

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


class TokenLogout(Resource):
    decorators = [token_auth.login_required]

    def post(self):
        user = token_auth.current_user()
        token = Token.query.filter_by(user=user.uid).first()
        db.session.delete(token)
        db.session.commit()
        return {"message": "success"}


class Register(Resource):

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


class ProfileList(Resource):
    decorators = [token_auth.login_required(role=["admin", "stuff"])]

    def get(self):
        args = pagination_parser.parse_args(request)
        page = args.get("page")
        size = args.get("size")
        pagination = User.query.filter_by().paginate(page=page,
                                                     per_page=size,
                                                     max_per_page=max_size)
        return {
            "count":
            pagination.total,
            "next":
            url_for("auth.profiles", page=pagination.next_num, _external=True)
            if pagination.has_next else None,
            "previous":
            url_for("auth.profiles", page=pagination.prev_num, _external=True)
            if pagination.has_prev else None,
            "results": [{
                "uid":
                item.uid,
                "username":
                item.username,
                "avatar":
                url_for("world.media", path=item.avatar, _external=True),
                "email":
                item.email,
            } for item in pagination.items]
        }


class ProfileDetail(Resource):
    decorators = [token_auth.login_required]

    def get(self):
        user = token_auth.current_user()
        item = User.query.filter_by(uid=user.uid).first()
        return {
            "uid": item.uid,
            "username": item.username,
            "email": item.email,
            "avatar": url_for("world.media", path=item.avatar, _external=True),
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
            "avatar": url_for("world.media", path=item.avatar, _external=True),
            "isAdmin": item.is_admin,
        }

    def delete(self):
        user = token_auth.current_user()
        item = User.query.filter_by(uid=user.uid).first()
        item.active = False
        db.session.commit()
        return {"message": "success"}


class ChangeAvatar(Resource):
    decorators = [token_auth.login_required]

    def post(self):
        user = token_auth.current_user()
        item = User.query.filter_by(uid=user.uid).first()
        if "avatar" not in request.files:
            return invalid_api_usage("No avatar provided", 400)
        file = request.files["avatar"]
        if not User.allow_avatar_file(file.filename):
            return invalid_api_usage("Invalid avatar", 400)
        filename = secure_filename(file.filename)
        item.delete_avatar_file()
        item.avatar = item.avatar_upload_to(filename)
        file.save(
            os.path.join(current_app.config["UPLOAD_FOLDER"], item.avatar))
        db.session.commit()
        return {"message": "success"}


api.add_resource(TokenLogin, "/token/login", endpoint="token-login")
api.add_resource(TokenLogout, "/token/logout", endpoint="token-logout")
api.add_resource(Register, "/register", endpoint="register")
api.add_resource(ProfileList, "/users", endpoint="profiles")
api.add_resource(ProfileDetail, "/users/profile", endpoint="profile-detail")
api.add_resource(ChangeAvatar,
                 "/users/profile/change/avatar",
                 endpoint="change-avatar")
