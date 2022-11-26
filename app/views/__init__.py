from flask import Blueprint
from flask.app import Flask
from flask.helpers import url_for
from flask.views import MethodView

from app.views import auth, blog
from app.utils.error import page_not_found

bp = Blueprint("world", __name__, url_prefix="/")
bp.register_blueprint(auth.bp)
bp.register_blueprint(blog.bp)
bp.add_url_rule("/media/<path:path>", endpoint="media", build_only=True)


def init_app(app: Flask):
    app.register_error_handler(404, page_not_found)


class Root(MethodView):

    def get(self) -> dict:
        return {
            "articles": url_for("world.blog.articles", _external=True),
        }


bp.add_url_rule("/", view_func=Root.as_view("root"))
