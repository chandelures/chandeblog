from flask import Blueprint, current_app
from flask.helpers import send_from_directory, url_for
from flask_restful import Resource, Api

from app.views import auth, blog

bp = Blueprint("world", __name__, url_prefix="/")
bp.register_blueprint(auth.bp)
bp.register_blueprint(blog.bp)
api = Api(bp)


class Root(Resource):
    def get(self) -> dict:
        return {
            "articles": url_for("blog.articles", _external=True),
            "categories": url_for("blog.categories", _external=True)
        }


@bp.route("/media/<path:path>", build_only=True)
def media(path):
    return send_from_directory(
        directory=current_app.config["UPLOAD_FOLDER"],
        path=path
    )


api.add_resource(Root, "/")
