import pytest

import tempfile

from app import create_app
from app.models import db


@pytest.fixture
def app():
    app = create_app({
        "TESTTING": True,
        "DATABASE": tempfile.mkstemp(),
    })

    with app.app_context():
        db.create_all()

    return app


@pytest.fixture
def client(app):
    return app.test_client()
