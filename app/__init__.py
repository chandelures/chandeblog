import os
from pathlib import Path
from flask import Flask
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parent.parent


def create_app(test_config=None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SITENAME="BlogApi",
        SQLALCHEMY_DATABASE_URI="sqlite:////{}/db.sqlite3".format(
            app.instance_path),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=os.path.join(BASE_DIR, "media"),
        MAX_CONTENT_LENGTH=16 * 1000 * 1000,
        ORIGINS=[],
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(app, supports_credentials=True, origins=app.config.get("ORIGINS"))

    from app.models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    from app.views import bp, init_app
    app.register_blueprint(bp)
    init_app(app)

    from app.utils import init_app
    init_app(app)

    from app.admin import init_app
    init_app(app)

    return app
