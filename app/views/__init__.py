from flask import Blueprint
from flask.app import Flask
from flask.helpers import url_for
from flask_restful import Resource, Api

from app.views import auth, blog
from app.utils.error import page_not_found

bp = Blueprint("world", __name__, url_prefix="/")
bp.register_blueprint(auth.bp)
bp.register_blueprint(blog.bp)
bp.add_url_rule("/media/<path:path>", endpoint="media", build_only=True)
api = Api(bp)


def init_app(app: Flask):
    app.register_error_handler(404, page_not_found)


class Root(Resource):

    def get(self) -> dict:
        return {
            "articles": url_for("blog.articles", _external=True),
            "categories": url_for("blog.categories", _external=True)
        }


api.add_resource(Root, "/")
