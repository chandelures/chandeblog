from flask import Blueprint, request, url_for
from flask.views import MethodView

from webargs.flaskparser import parser

from app.utils.args import pagination_args
from app.utils.auth import token_auth
from app.models import db
from app.models.blog import Article, Category, About
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
        category = data.get("category")
        author = token_auth.current_user()
        if not title or not abstract or not content:
            return invalid_api_usage("No title, abstract or content provided",
                                     400)
        if Article.query.filter_by(title=title).first():
            return invalid_api_usage("Title is already exist", 400)
        item = Article(title,
                       abstract,
                       content,
                       category=category,
                       author=author.uid)
        item.author = author.uid
        db.session.add(item)
        db.session.commit()
        return {
            "title": item.title,
            "abstract": item.abstract,
            "content": item.content,
            "category": item.category,
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
            "category": item.category,
            "next": next.slug if next else None,
            "previous": previous.slug if previous else None,
        }

    @token_auth.login_required(role=["admin", "stuff"])
    def put(self, slug):
        data = request.get_json() or {}
        title = data.get("title")
        abstract = data.get("abstract")
        content = data.get("content")
        category = data.get("category")
        item = Article.query.filter_by(slug=slug).first()
        attrs = dict(title=title,
                     abstract=abstract,
                     content=content,
                     category=category)
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
            "category": item.category,
        }

    @token_auth.login_required(role=["admin", "stuff"])
    def delete(self, slug):
        item = Article.query.filter_by(slug=slug).first()
        if not item:
            return invalid_api_usage("No such article", 204)
        db.session.delete(item)
        db.session.commit()
        return {"message": "success"}


class CategoryList(MethodView):

    @parser.use_args(pagination_args, location="query")
    def get(self, args):
        pagination = Category.query.filter_by().paginate(
            page=args["page"],
            per_page=args["size"],
        )
        return {
            "count":
            pagination.total,
            "next":
            url_for("world.blog.categories",
                    page=pagination.next_num,
                    _external=True) if pagination.has_next else None,
            "previous":
            url_for("world.blog.categories",
                    page=pagination.prev_num,
                    _external=True) if pagination.has_prev else None,
            "results": [{
                "name": item.name,
                "slug": item.slug,
            } for item in pagination.items],
        }


class CategoryCreate(MethodView):

    @token_auth.login_required(role=["admin", "stuff"])
    def post(self):
        data = request.get_json() or {}
        name = data.get("name")
        if not name:
            return invalid_api_usage("No name provided", 400)
        if Category.query.filter_by(name=name).first():
            return invalid_api_usage("Name is already exist", 400)
        category = Category(name)
        db.session.add(category)
        db.session.commit()
        return {
            "name": category.name,
            "slug": category.slug,
        }, 201


class CategoryDetail(MethodView):

    def get(self, slug):
        item = Category.query.filter_by(slug=slug).first()
        if not item:
            return invalid_api_usage("No such category", 404)
        return {
            "name":
            item.name,
            "slug":
            item.slug,
            "articles":
            [{
                "title": article.title,
                "abstract": article.abstract,
                "slug": article.slug,
                "authorName":
                User.query.filter_by(uid=article.author).first().username,
                "item": article.category,
                "created": article.created.isoformat(),
                "updated": article.updated.isoformat(),
                "views": article.views,
            }
             for article in Article.query.filter_by(category=item.slug).all()],
        }

    @token_auth.login_required(role=["admin", "stuff"])
    def put(self, slug):
        data = request.get_json() or {}
        name = data.get("name")
        item = Category.query.filter_by(slug=slug).first()
        if name:
            item.name = name
        item.update_slug()
        db.session.commit()
        return {"message": "success"}

    @token_auth.login_required(role=["admin", "stuff"])
    def delete(self, slug):
        item = Category.query.filter_by(slug=slug).first()
        if not item:
            return invalid_api_usage("No such category", 204)
        articles = Article.query.filter_by(category=slug).all()
        for article in articles:
            article.category = None
        db.session.delete(item)
        db.session.commit()
        return {"message": "success"}


class AboutView(MethodView):

    def get(self):
        about = About.query.first()
        if not about:
            return invalid_api_usage("No article is associated with about",
                                     404)
        article = Article.query.filter_by(slug=about.article).first()
        if not article:
            return invalid_api_usage("No such article", 404)
        author = User.query.filter_by(uid=article.author).first()
        return {
            "title": article.title,
            "abstract": article.abstract,
            "content": article.content,
            "slug": article.slug,
            "created": article.created.isoformat(),
            "updated": article.updated.isoformat(),
            "authorName": author.username,
            "avatar": url_for("world.media",
                              path=author.avatar,
                              _external=True),
            "category": article.category,
        }

    @token_auth.login_required(role=["admin", "stuff"])
    def post(self):
        data = request.get_json() or {}
        article = data.get("article")
        if not article:
            return invalid_api_usage("No article provided", 400)
        if not Article.query.filter_by(slug=article).first():
            return invalid_api_usage("Article is not exist", 400)
        about = About.query.first()
        if about:
            about.article = article
        else:
            about = About(article)
            db.session.add(about)
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
bp.add_url_rule("/categories",
                view_func=CategoryList.as_view("categories"),
                endpoint="categories")
bp.add_url_rule("/categories",
                view_func=CategoryCreate.as_view("category-create"),
                endpoint="category-create")
bp.add_url_rule("/categories/<string:slug>",
                view_func=CategoryDetail.as_view("category-detail"),
                endpoint="category-detail")
bp.add_url_rule("/about",
                view_func=AboutView.as_view("about"),
                endpoint="about")
