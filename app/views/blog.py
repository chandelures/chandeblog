from flask import Blueprint
from flask_restful import Api, Resource

from app.utils.auth import token_auth
from app.models.blog import Article, Category, About

bp = Blueprint("blog", __name__, url_prefix="/")
api = Api(bp)


class ArticleList(Resource):
    def get(self):
        pass


class ArticleCreate(Resource):
    @token_auth.login_required(role=["admin", "stuff"])
    def post(self):
        pass


class ArticleDetail(Resource):
    def get(self):
        pass

    @token_auth.login_required(role=["admin", "stuff"])
    def put(self):
        pass

    @token_auth.login_required(role=["admin", "stuff"])
    def delete(self):
        pass


class CategoryList(Resource):
    def get(self):
        pass


class CategoryCreate(Resource):
    @token_auth.login_required(role=["admin", "stuff"])
    def post(self):
        pass


class CategoryDetail(Resource):
    def get(self):
        pass

    @token_auth.login_required(role=["admin", "stuff"])
    def put(self):
        pass

    @token_auth.login_required(role=["admin", "stuff"])
    def delete(self):
        pass


class About(Resource):
    def get(self):
        pass

    @token_auth.login_required(role=["admin", "stuff"])
    def post(self):
        pass


api.add_resource(ArticleList, "/articles")
api.add_resource(ArticleCreate, "/articles/create")
api.add_resource(ArticleDetail, "/articles/<string:slug>")
api.add_resource(CategoryList, "/categories")
api.add_resource(CategoryCreate, "/categories/create")
api.add_resource(CategoryCreate, "/categories/<string:slug>")
api.add_resource(About, "/about")
