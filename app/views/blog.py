from flask import Blueprint, request, url_for
from flask.views import MethodView

from webargs.flaskparser import parser

from app.utils.args import pagination_args
from app.utils.auth import token_auth
from app.models import db
from app.models.blog import Article
from app.models.auth import User
from app.utils.error import invalid_api_usage

bp = Blueprint("blog", __name__, url_prefix="/")


class ArticleList(MethodView):

    @parser.use_args(pagination_args, location="query")
    def get(self, args):
        pagination = Article.query.order_by(Article.created.desc()).paginate(
            page=args["page"], per_page=args["size"])
        return {
            "count":
            pagination.total,
            "next":
            url_for("world.blog.articles",
                    page=pagination.next_num,
                    _external=True) if pagination.has_next else None,
            "previous":
            url_for("world.blog.articles",
                    page=pagination.prev_num,
                    _external=True) if pagination.has_prev else None,
            "results": [{
                "title":
                item.title,
                "abstract":
                item.abstract,
                "slug":
                item.slug,
                "authorName":
                User.query.filter_by(uid=item.author).first().username,
                "created":
                item.created.isoformat(),
                "updated":
                item.updated.isoformat(),
                "views":
                item.views,
            } for item in pagination.items],
        }


class ArticleCreate(MethodView):

    @token_auth.login_required(role=["admin", "stuff"])
    def post(self):
        data = request.get_json() or {}
        title = data.get("title")
        abstract = data.get("abstract")
        content = data.get("content")
        author = token_auth.current_user()
        if not title or not abstract or not content:
            return invalid_api_usage("No title, abstract or content provided",
                                     400)
        if Article.query.filter_by(title=title).first():
            return invalid_api_usage("Title is already exist", 400)
        item = Article(title, abstract, content, author=author.uid)
        item.author = author.uid
        db.session.add(item)
        db.session.commit()
        return {
            "title": item.title,
            "abstract": item.abstract,
            "content": item.content,
            "slug": item.slug,
            "authorName":
            User.query.filter_by(uid=item.author).first().username,
            "created": item.created.isoformat(),
            "updated": item.updated.isoformat(),
        }, 201


class ArticleDetail(MethodView):

    def get(self, slug):
        item = Article.query.filter_by(slug=slug).first()
        if not item:
            return invalid_api_usage("No such article", 404)
        next = Article.query.filter(Article.created > item.created).order_by(
            Article.created).first()
        previous = Article.query.filter(
            Article.created < item.created).order_by(
                Article.created.desc()).first()
        author = User.query.filter_by(uid=item.author).first()
        return {
            "title": item.title,
            "abstract": item.abstract,
            "content": item.content,
            "slug": item.slug,
            "created": item.created.isoformat(),
            "updated": item.updated.isoformat(),
            "authorName": author.username,
            "avatar": url_for("world.media",
                              path=author.avatar,
                              _external=True),
            "next": next.slug if next else None,
            "previous": previous.slug if previous else None,
        }

    @token_auth.login_required(role=["admin", "stuff"])
    def put(self, slug):
        data = request.get_json() or {}
        title = data.get("title")
        abstract = data.get("abstract")
        content = data.get("content")
        item = Article.query.filter_by(slug=slug).first()
        attrs = dict(
            title=title,
            abstract=abstract,
            content=content,
        )
        for name, value in attrs.items():
            if value:
                setattr(item, name, value)
        item.update_slug()
        db.session.commit()
        return {
            "title": item.title,
            "abstract": item.abstract,
            "content": item.content,
            "slug": item.slug,
            "created": item.created.isoformat(),
            "updated": item.updated.isoformat(),
            "authorName":
            User.query.filter_by(uid=item.author).first().username,
        }

    @token_auth.login_required(role=["admin", "stuff"])
    def delete(self, slug):
        item = Article.query.filter_by(slug=slug).first()
        if not item:
            return invalid_api_usage("No such article", 204)
        db.session.delete(item)
        db.session.commit()
        return {"message": "success"}


bp.add_url_rule("/articles",
                view_func=ArticleList.as_view("articles"),
                endpoint="articles")
bp.add_url_rule("/articles",
                view_func=ArticleCreate.as_view("article-create"),
                endpoint="article-create")
bp.add_url_rule("/articles/<string:slug>",
                view_func=ArticleDetail.as_view("article-detail"),
                endpoint="article-detail")
