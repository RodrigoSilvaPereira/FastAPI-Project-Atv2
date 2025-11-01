from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_students_success():
    response = client.get("/students/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1  # Pelo menos o aluno inicial existe


def test_get_student_success():
    response = client.get("/students/1")
    assert response.status_code == 200
    student = response.json()
    assert student["id"] == 1
    assert student["name"] == "Roh"


def test_create_student_success():
    new_student = {"name": "Teste", "email": "teste@exemplo.com"}
    response = client.post("/students/", json=new_student)
    assert response.status_code == 200
    student = response.json()
    assert student["name"] == new_student["name"]
    assert student["email"] == new_student["email"]
    assert "id" in student


def test_get_student_not_found():
    response = client.get("/students/9999")  # ID inexistente
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


def test_create_student_missing_fields():
    incomplete_student = {"name": "Sem email"}
    response = client.post("/students/", json=incomplete_student)
    assert response.status_code == 400
    assert response.json()["detail"] == "Missing name or email"
