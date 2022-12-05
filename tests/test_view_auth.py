import pytest

from flask import Flask
from flask.testing import FlaskClient

from app.models.auth import Token, User


@pytest.mark.parametrize(
    (
        "username",
        "password",
        "status_code",
    ),
    (("", "", 400), ("admin", "", 400), ("not_exists", "not_exists", 400),
     ("admin", "admin", 200), ("admin@admin.org", "admin", 200),
     ("admin", "adminn", 400)),
)
def test_token_login(client: FlaskClient, username: str, password: str,
                     status_code: int) -> None:
    url = "/auth/token/login"
    res = client.post(url, json={
        "username": username,
        "password": password,
    })
    assert res.is_json
    assert res.status_code == status_code
    token = res.get_json().get("token")
    res = client.post(url, json={
        "username": username,
        "password": password,
    })
    assert res.is_json
    assert res.get_json().get("token") == token


def test_token_logout(client: FlaskClient, stuff_client: FlaskClient,
                      app: Flask) -> None:
    url = "/auth/token/logout"
    res = client.post(url)
    assert res.is_json
    assert res.status_code == 401

    res = stuff_client.post(url)
    assert res.is_json
    assert res.status_code == 200
    with app.app_context():
        user = User.query.filter_by(username="admin").first()
        token = Token.query.filter_by(user=user.uid).first()
    assert not token


@pytest.mark.parametrize(("username", "email", "password", "status_code"),
                         (("", "", "", 400), ("user1", "", "", 400),
                          ("user2", "user2@user2.org", "", 400),
                          ("user3", "user3@user3.org", "psw", 400),
                          ("user4", "user4@user4.org", "validpassword", 201)))
def test_register(client: FlaskClient, app: Flask, username: str, email: str,
                  password: str, status_code: int) -> None:
    res = client.post("/auth/register",
                      json={
                          "username": username,
                          "email": email,
                          "password": password,
                      })
    assert res.is_json
    assert res.status_code == status_code

    if status_code == 400:
        return

    with app.app_context():
        user = User.query.filter_by(username=username).first()
        assert user
        assert user.username == username
        assert user.email == email
        assert user.password


def test_get_profile_list(client: FlaskClient, user_client: FlaskClient,
                          stuff_client: FlaskClient) -> None:
    url = "/auth/users"
    res = client.get(url)
    assert res.is_json
    assert res.status_code == 401

    res = user_client.get(url)
    assert res.is_json
    assert res.status_code == 403

    res = stuff_client.get(url)
    assert res.is_json
    assert res.status_code == 200


def test_get_profile_detail(client: FlaskClient,
                            user_client: FlaskClient) -> None:
    url = "/auth/users/profile"
    res = client.get(url)
    assert res.is_json
    assert res.status_code == 401

    res = user_client.get(url)
    assert res.is_json
    assert res.status_code == 200


@pytest.mark.parametrize(("data", "status_code"), (
    ({
        "username": "othername",
    }, 400),
    ({
        "email": "otheremail@user.org"
    }, 400),
    ({
        "username": "othername",
        "email": "otheremail@user.org",
    }, 200),
))
def test_update_profile_detail(client: FlaskClient, user_client: FlaskClient,
                               app: Flask, data: dict,
                               status_code: int) -> None:
    url = "/auth/users/profile"
    res = client.put(url)
    assert res.is_json
    assert res.status_code == 401

    res = user_client.put(url, json=data)
    assert res.is_json
    assert res.status_code == status_code

    if status_code == 400:
        return

    with app.app_context():
        user = User.query.filter_by(username=data.get("username")).first()
    assert user
    assert user.username == data.get("username")
    assert user.email == data.get("email")


def test_delete_user(client: FlaskClient, user_client: FlaskClient,
                     app: Flask) -> None:
    url = "/auth/users/profile"
    res = client.delete(url)
    assert res.is_json
    assert res.status_code == 401

    res = user_client.delete(url)
    assert res.is_json
    assert res.status_code == 200

    with app.app_context():
        user = User.query.filter_by(username="temp").first()
    assert user
    assert not user.active

    res = user_client.post("/auth/token/logout")
    res = user_client.post("/auth/token/login",
                           json={
                               "username": "temp",
                               "password": "temppsw"
                           })
    assert res.is_json
    assert res.status_code == 400
