import os
from pathlib import Path
from flask import Flask

BASE_DIR = Path(__file__).resolve().parent.parent


def create_app(test_config=None) -> Flask:
    app = Flask("chandeblog", instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:////{}/db.sqlite3".format(
            app.instance_path
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=os.path.join(BASE_DIR, "media"),
        MAX_CONTENT_LENGTH=16*1000*1000,
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
        os.makedirs(app.config["UPLOAD_FOLDER"])
    except OSError:
        pass

    from app.models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    from app.views import bp
    app.register_blueprint(bp)

    return app
