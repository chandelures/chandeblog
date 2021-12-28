from app.utils import slugify


def test_slugify():
    s = "test test test"
    assert " " not in slugify(s)
    s = "测试 测试 测试"
    assert " " not in slugify(s)
