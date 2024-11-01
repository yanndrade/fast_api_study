import pytest
from fastapi.testclient import TestClient

from fastapizero.app import app


@pytest.fixture
def client():  # Arrange
    return TestClient(app)
