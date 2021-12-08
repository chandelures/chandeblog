from flask_restful import reqparse

pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument("page", type=int, default=1, required=False)
pagination_parser.add_argument("size", type=int, default=10, required=False)

max_size = 50
