from starlette.testclient import TestClient


def test_meta(testclient: TestClient) -> None:
    """Ensure that the api endpoint returns API metadata."""
    response = testclient.get("/api/")
    json = response.json()
    assert isinstance(json, dict)
    assert json["name"] == "Sage"
    assert "version" in json
    assert "contact" in json
