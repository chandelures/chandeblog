from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

from app.models.auth import *  # NOQA
from app.models.blog import *  # NOQA
