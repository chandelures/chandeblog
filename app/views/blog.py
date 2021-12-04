from flask import Blueprint
from flask_restful import Api, Resource

bp = Blueprint("blog", __name__, url_prefix="/")
api = Api(bp)
