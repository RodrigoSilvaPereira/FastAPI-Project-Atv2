import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Fixture para fornecer o cliente de teste do FastAPI."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_external_data():
    """Fixture com dados mockados para simular a API externa."""
    return [
        {"userId": 1, "id": 1, "title": "Test Title 1", "body": "Test body content 1"},
        {"userId": 1, "id": 2, "title": "Test Title 2", "body": "Test body content 2"},
    ]


@pytest.fixture
def mock_single_data():
    """Fixture com um único item mockado."""
    return {
        "userId": 1,
        "id": 1,
        "title": "Test Title 1",
        "body": "Test body content 1",
    }


@pytest.fixture
def mock_new_data():
    """Fixture com dados para criação de novo item."""
    return {"title": "New Post", "body": "New post content", "userId": 1}


@pytest.fixture
def mock_created_data():
    """Fixture com resposta mockada para criação bem-sucedida."""
    return {"id": 101, "title": "New Post", "body": "New post content", "userId": 1}


class TestGetAllData:
    """Testes para a rota GET /api/data/"""

    @patch("app.routes.data_routes.fetch_all_data")
    def test_get_all_data_success(self, mock_fetch, client, mock_external_data):
        """Teste de sucesso para listar todos os dados."""
        # Mock da função assíncrona
        mock_fetch.return_value = mock_external_data

        # Executa a requisição
        response = client.get("/api/data/")

        # Verificações
        assert response.status_code == 200
        assert response.json() == mock_external_data
        mock_fetch.assert_called_once()

    @patch("app.routes.data_routes.fetch_all_data")
    def test_get_all_data_failure(self, mock_fetch, client):
        """Teste de falha para listar todos os dados."""
        # Mock simulando uma exceção
        mock_fetch.side_effect = Exception("API externa indisponível")

        # Executa a requisição
        response = client.get("/api/data/")

        # Verificações
        assert response.status_code == 500
        assert "API externa indisponível" in response.json()["detail"]
        mock_fetch.assert_called_once()


class TestGetDataById:
    """Testes para a rota GET /api/data/{item_id}"""

    @patch("app.routes.data_routes.fetch_data_by_id")
    def test_get_data_by_id_success(self, mock_fetch, client, mock_single_data):
        """Teste de sucesso para buscar dado por ID."""
        # Mock da função assíncrona
        mock_fetch.return_value = mock_single_data

        # Executa a requisição
        response = client.get("/api/data/1")

        # Verificações
        assert response.status_code == 200
        assert response.json() == mock_single_data
        mock_fetch.assert_called_once_with(1)

    @patch("app.routes.data_routes.fetch_data_by_id")
    def test_get_data_by_id_not_found(self, mock_fetch, client):
        """Teste de falha para buscar dado por ID (não encontrado)."""
        # Mock simulando item não encontrado
        mock_fetch.return_value = None

        # Executa a requisição
        response = client.get("/api/data/999")

        # Verificações
        assert response.status_code == 404
        assert response.json()["detail"] == "Item not found"
        mock_fetch.assert_called_once_with(999)

    @patch("app.routes.data_routes.fetch_data_by_id")
    def test_get_data_by_id_external_error(self, mock_fetch, client):
        """Teste de falha para buscar dado por ID (erro na API externa)."""
        # Mock simulando erro na API externa
        mock_fetch.side_effect = Exception("Erro de conexão")

        # Executa a requisição
        response = client.get("/api/data/1")

        # Verificações
        assert response.status_code == 500
        assert "Erro de conexão" in response.json()["detail"]
        mock_fetch.assert_called_once_with(1)


class TestPostNewData:
    """Testes para a rota POST /api/data/"""

    @patch("app.routes.data_routes.create_data")
    def test_post_new_data_success(
        self, mock_create, client, mock_new_data, mock_created_data
    ):
        """Teste de sucesso para criar novo dado."""
        # Mock da função assíncrona
        mock_create.return_value = mock_created_data

        # Executa a requisição
        response = client.post("/api/data/", json=mock_new_data)

        # Verificações
        assert response.status_code == 200
        assert response.json() == mock_created_data
        mock_create.assert_called_once_with(mock_new_data)

    @patch("app.routes.data_routes.create_data")
    def test_post_new_data_failure(self, mock_create, client, mock_new_data):
        """Teste de falha para criar novo dado."""
        # Mock simulando erro na criação
        mock_create.side_effect = Exception("Falha na criação do dado")

        # Executa a requisição
        response = client.post("/api/data/", json=mock_new_data)

        # Verificações
        assert response.status_code == 500
        assert "Falha na criação do dado" in response.json()["detail"]
        mock_create.assert_called_once_with(mock_new_data)


class TestRootEndpoint:
    """Testes para a rota raiz GET /"""

    def test_root_endpoint_success(self, client):
        """Teste de sucesso para a rota raiz."""
        response = client.get("/")

        assert response.status_code == 200
        assert response.json() == {"message": "API is running successfully 🚀"}
