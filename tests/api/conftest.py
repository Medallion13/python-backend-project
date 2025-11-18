""" Configuracion para test del API"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.schemas.users import UserCreate, UserResponse


@pytest.fixture
def sample_user() -> UserCreate:
    return UserCreate(username="Test User", email="test@test.com", password="Test password")


@pytest.fixture
def created_user(client: TestClient, sample_user: UserCreate) -> UserResponse:
    create_response = client.post("/users", json=sample_user.model_dump())
    assert create_response.status_code == status.HTTP_201_CREATED
    data = create_response.json()
    return UserResponse.model_validate(data)
