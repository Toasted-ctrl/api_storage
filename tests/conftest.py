import pytest

from fastapi.testclient import TestClient

from tests.fixtures.auth import *
from tests.fixtures.services import *

@pytest.fixture
def app():
    from main import app
    yield app
    app.dependency_overrides.clear()

@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c