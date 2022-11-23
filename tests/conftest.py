import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient


@pytest.fixture()
def app() -> FastAPI:
    """Fixture for the app itself."""
    from sage.app import app

    return app


@pytest.fixture
def testclient(app: FastAPI) -> TestClient:
    """Testclient for the app."""
    return TestClient(app)
