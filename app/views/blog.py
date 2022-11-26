from flask import Blueprint, request, url_for
from flask.views import MethodView

from webargs.flaskparser import parser

from app.utils.args import pagination_args
from app.utils.auth import token_auth
from app.models import db
from app.models.blog import Post
from app.models.auth import User
from app.utils.error import invalid_api_usage

bp = Blueprint("blog", __name__, url_prefix="/")


class PostList(MethodView):

    @parser.use_args(pagination_args, location="query")
    def get(self, args):
        pagination = Post.query.order_by(Post.created.desc()).paginate(
            page=args["page"], per_page=args["size"])
        return {
            "count":
            pagination.total,
            "next":
            url_for("world.blog.posts",
                    page=pagination.next_num,
                    _external=True) if pagination.has_next else None,
            "previous":
            url_for("world.blog.posts",
                    page=pagination.prev_num,
                    _external=True) if pagination.has_prev else None,
            "results": [{
                "title":
                item.title,
                "description":
                item.description,
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


class PostCreate(MethodView):

    @token_auth.login_required(role=["admin", "stuff"])
    def post(self):
        data = request.get_json() or {}
        title = data.get("title")
        description = data.get("description")
        content = data.get("content")
        author = token_auth.current_user()
        if not title or not description or not content:
            return invalid_api_usage(
                "No title, description or content provided", 400)
        if Post.query.filter_by(title=title).first():
            return invalid_api_usage("Title is already exist", 400)
        item = Post(title, description, content, author=author.uid)
        item.author = author.uid
        db.session.add(item)
        db.session.commit()
        return {
            "title": item.title,
            "description": item.description,
            "content": item.content,
            "slug": item.slug,
            "authorName":
            User.query.filter_by(uid=item.author).first().username,
            "created": item.created.isoformat(),
            "updated": item.updated.isoformat(),
        }, 201


class PostDetail(MethodView):

    def get(self, slug):
        item = Post.query.filter_by(slug=slug).first()
        if not item:
            return invalid_api_usage("No such post", 404)
        next = Post.query.filter(Post.created > item.created).order_by(
            Post.created).first()
        previous = Post.query.filter(Post.created < item.created).order_by(
            Post.created.desc()).first()
        author = User.query.filter_by(uid=item.author).first()
        return {
            "title": item.title,
            "description": item.description,
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
        description = data.get("description")
        content = data.get("content")
        item = Post.query.filter_by(slug=slug).first()
        attrs = dict(
            title=title,
            description=description,
            content=content,
        )
        for name, value in attrs.items():
            if value:
                setattr(item, name, value)
        item.update_slug()
        db.session.commit()
        return {
            "title": item.title,
            "description": item.description,
            "content": item.content,
            "slug": item.slug,
            "created": item.created.isoformat(),
            "updated": item.updated.isoformat(),
            "authorName":
            User.query.filter_by(uid=item.author).first().username,
        }

    @token_auth.login_required(role=["admin", "stuff"])
    def delete(self, slug):
        item = Post.query.filter_by(slug=slug).first()
        if not item:
            return invalid_api_usage("No such post", 204)
        db.session.delete(item)
        db.session.commit()
        return {"message": "success"}


bp.add_url_rule("/posts",
                view_func=PostList.as_view("posts"),
                endpoint="posts")
bp.add_url_rule("/posts",
                view_func=PostCreate.as_view("post-create"),
                endpoint="post-create")
bp.add_url_rule("/posts/<string:slug>",
                view_func=PostDetail.as_view("post-detail"),
                endpoint="post-detail")
