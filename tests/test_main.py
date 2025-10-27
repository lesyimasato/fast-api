from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_all_students_success():
    response = client.get("/students")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "name" in data[0]

def test_get_student_by_id_success():
    response = client.get("/students/1")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == 1

def test_create_student_success():
    response = client.post(
        "/students",
        json={
            "name": "Renato Hioji Okamoto Odake",
            "email": "renato.oodake@example.com",
        },
    )
    data = response.json()
    assert response.status_code == 201
    assert data["name"] == "Renato Hioji Okamoto Odake"

def test_get_student_by_id_not_found():
    response = client.get("/students/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Student not found"}

def test_create_student_duplicate_email():
    client.post(
        "/students",
        json={"name": "Letícia Sayuri Imasato", "email": "leticia.sayuri@example.com"},
    )
    response = client.post(
        "/students",
        json={"name": "Letícia Sayuri Okamoto", "email": "leticia.sayuri@example.com"},
    )
    assert response.status_code == 400
    assert "Already exists" in response.json()["detail"]
