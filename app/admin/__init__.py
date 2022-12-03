from flask import Flask
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

from app.models.blog import Post
from app.models.auth import User
from app.models import db
from app.utils.auth import base_auth


class AuthAdminIndexView(AdminIndexView):

    @base_auth.login_required
    @expose('/')
    def index(self):
        return super().index()


class AuthModelView(ModelView):

    def is_accessible(self):
        auth = base_auth.get_auth()
        password = base_auth.get_auth_password(auth)
        user = base_auth.authenticate(auth, stored_password=password)
        if user:
            return True
        return False


def init_app(app: Flask):
    admin = Admin(app,
                  index_view=AuthAdminIndexView(),
                  name=app.config["SITENAME"],
                  template_mode="bootstrap4")
    admin.add_view(AuthModelView(Post, db.session))
    admin.add_view(ModelView(User, db.session))
