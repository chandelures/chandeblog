import pytest
from flask.app import Flask
from flask.testing import FlaskCliRunner

from app.models.auth import User


@pytest.mark.parametrize(
    ("username", "email", "password", "output"),
    (("", "", "", "Failed"), ("superuser", "", "", "Failed"),
     ("superuser", "superuser@test.org", "", "Failed"),
     ("superuser", "superuser@test.org", "admin", "Created")))
def test_create_superuser(runner: FlaskCliRunner, app: Flask, username: str,
                          email: str, password: str, output: str) -> None:
    result = runner.invoke(args=[
        "createsuperuser", "--username", username, "--email", email,
        "--password", password
    ])
    assert output in result.output

    if output != "Created":
        return

    with app.app_context():
        user = User.query.filter_by(username=username).first()
    assert user
    assert user.stuff
    assert user.superuser
