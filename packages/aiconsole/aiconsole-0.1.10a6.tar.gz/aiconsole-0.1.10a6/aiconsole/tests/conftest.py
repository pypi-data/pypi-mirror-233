import pytest
from fastapi.testclient import TestClient

from aiconsole.app import app as fastapi_app


@pytest.fixture()
def app():
    return fastapi_app


@pytest.fixture()
def client(app):
    return TestClient(app)
