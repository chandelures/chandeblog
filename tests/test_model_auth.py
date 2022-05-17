from app.models.auth import User


def test_user_representation() -> None:
    user = User("test", "test@test.org")
    assert isinstance(user.__repr__(), str)


def test_user_roles() -> None:
    user = User("test", "test@test.org")
    assert user.get_roles() == "ordinary"
    user.stuff = True
    assert user.get_roles() == "stuff"
    user.superuser = True
    assert user.get_roles() == "admin"
