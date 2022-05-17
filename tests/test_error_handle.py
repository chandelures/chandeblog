from flask.testing import FlaskClient


def test_page_not_found(client: FlaskClient) -> None:
    url = "not-exists-url"
    res = client.get(url)
    assert res.is_json
    assert res.status_code == 404
