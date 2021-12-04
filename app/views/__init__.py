from flask import Blueprint
from flask_restful import Resource, Api

from app.utils.auth import token_auth

bp = Blueprint("world", __name__, url_prefix="/")
api = Api(bp)


class Root(Resource):
    decorators = [token_auth.login_required(role=["admin"])]

    def get(self) -> dict:
        return {
            "hello": "world",
            "user": token_auth.current_user().username
        }


api.add_resource(Root, "/")
