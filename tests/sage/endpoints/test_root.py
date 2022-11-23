from starlette.testclient import TestClient


def test_root(testclient: TestClient) -> None:
    """Ensure that the root endpoint redirects properly to the metadata endpoint."""
    response = testclient.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.has_redirect_location
    assert response.headers["location"] == "/api/"
