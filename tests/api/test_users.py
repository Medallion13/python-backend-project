from fastapi import status
from fastapi.testclient import TestClient

from app.models import UserCreate, UserResponse, UserUpdate


# Testing POST /users/{user_id} endpoint
def test_create_user(client: TestClient, sample_user: UserCreate) -> None:
    response = client.post("/users", json=sample_user.model_dump())

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == sample_user.username
    assert data["email"] == sample_user.email
    assert "id" in data
    assert "password" not in data


def test_create_user_missing_password(client: TestClient) -> None:
    invalid_payload = {"username": "test", "email": "test@test.com"}

    response = client.post("/users", json=invalid_payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    data = response.json()
    assert data["detail"][0]["msg"] == "Field required"
    assert data["detail"][0]["loc"] == ["body", "password"]


# Testing POST /users/{user_id} endpoint
def test_get_user_by_id(client: TestClient, created_user: UserResponse) -> None:
    user_id = created_user.id

    response = client.get(f"/users/{user_id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == created_user.username
    assert "password" not in data


def test_get_user_not_found(client: TestClient) -> None:
    response = client.get("/users/99999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


# Testing PUT /users/{user_id}
def test_update_user(client: TestClient, created_user: UserResponse) -> None:
    user_id = created_user.id

    update_payload = UserUpdate(username="new_username", email="new_email")
    response = client.put(f"/users/{user_id}", json=update_payload.model_dump(exclude_unset=True))

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == update_payload.username
    assert data["email"] == update_payload.email


def test_partial_update_user(client: TestClient, created_user: UserResponse) -> None:
    user_id = created_user.id

    update_payload = UserUpdate(username="new_username")
    response = client.put(f"/users/{user_id}", json=update_payload.model_dump(exclude_unset=True))

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == update_payload.username
    assert data["email"] == created_user.email


def test_update_user_not_found(client: TestClient) -> None:
    update_payload = UserUpdate(username="user_name")
    response = client.put("/users/99999", json=update_payload.model_dump(exclude_unset=True))

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


# Testing DELETE /users/{user_id}
def test_delete_user(client: TestClient, created_user: UserResponse) -> None:
    user_id = created_user.id

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user_not_found(client: TestClient) -> None:
    response = client.delete("/users/999999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}
