from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from app.models.blog import Post
from app.models.auth import User
from app.models import db
from app.utils.auth import base_auth


class AuthAdminIndexView(AdminIndexView):

    def is_accessible(self):
        auth = base_auth.get_auth()
        password = base_auth.get_auth_password(auth)
        user = base_auth.authenticate(auth, stored_password=password)
        if user:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return base_auth.auth_error_callback(status=401)


class AuthModelView(ModelView):

    def is_accessible(self):
        auth = base_auth.get_auth()
        password = base_auth.get_auth_password(auth)
        user = base_auth.authenticate(auth, stored_password=password)
        if user:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return base_auth.auth_error_callback(status=401)


class PostModelView(AuthModelView):
    column_exclude_list = ("description", "content", "slug")
    column_default_sort = ("created", True)

    def after_model_change(self, form, model, is_created):
        model.update_slug()
        self.session.commit()


class UserModelView(AuthModelView):
    column_exclude_list = ("password")


def init_app(app: Flask):
    admin = Admin(app,
                  index_view=AuthAdminIndexView(),
                  name=app.config["SITENAME"],
                  template_mode="bootstrap4")
    admin.add_view(PostModelView(Post, db.session))
    admin.add_view(UserModelView(User, db.session))
