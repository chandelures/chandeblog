from flask.testing import FlaskClient


def test_page_not_found(client: FlaskClient):
    url = "not-exists-url"
    res = client.get(url)
    assert res.status_code == 404
    assert res.is_json
