from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_student_by_id_success():
    response = client.get("/students/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Letícia Sayuri Imasato"}


def test_get_student_by_id_not_found():
    response = client.get("/students/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Student not found"}
