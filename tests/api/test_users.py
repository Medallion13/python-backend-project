from fastapi.testclient import TestClient

from app.models import UserCreate


def test_create_user(client: TestClient, sample_user: UserCreate) -> None:
    response = client.post("/users", json=sample_user.model_dump())

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == sample_user.username
    assert data["email"] == sample_user.email
    assert "id" in data
    assert "password" not in data


def test_create_user_missing_password(client: TestClient) -> None:
    invalid_payload = {"username": "test", "email": "test@test.com"}

    response = client.post("/users", json=invalid_payload)

    assert response.status_code == 422

    data = response.json()
    assert data["detail"][0]["msg"] == "Field required"
    assert data["detail"][0]["loc"] == ["body", "password"]
