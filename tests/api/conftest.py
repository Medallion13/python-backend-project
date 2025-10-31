""" Configuracion para test del API"""

import pytest
from fastapi.testclient import TestClient

from app.models import UserCreate, UserResponse


@pytest.fixture
def sample_user() -> UserCreate:
    return UserCreate(username="Test User", email="test@test.com", password="Test password")


@pytest.fixture
def created_user(client: TestClient, sample_user: UserCreate) -> UserResponse:
    create_response = client.post("/users", json=sample_user.model_dump())
    assert create_response.status_code == 201
    data = create_response.json()
    return UserResponse.model_validate(data)
