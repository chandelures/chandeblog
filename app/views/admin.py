from flask import Blueprint
from flask_restful import Api, Resource

bp = Blueprint("admin", __name__, url_prefix="/admin")
api = Api(bp)
