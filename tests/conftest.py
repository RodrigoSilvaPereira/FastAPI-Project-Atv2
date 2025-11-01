import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Fixture para fornecer o cliente de teste do FastAPI."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_payload():
    """Fixture com payload de exemplo para testes POST."""
    return {"title": "Test Post", "body": "This is a test post body", "userId": 1}
