from flask import Flask


def page_not_found(error):
    return {"detail": "This url does not found on the server"}, 404


class Error(object):

    def __init__(self, app: Flask) -> None:
        self.init_app(app)

    def init_app(self, app: Flask) -> None:
        app.register_error_handler(404, page_not_found)
