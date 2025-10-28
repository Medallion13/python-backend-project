""" Configuracion para test del API"""

import pytest

from app.models import UserCreate


@pytest.fixture
def sample_user() -> UserCreate:
    return UserCreate(username="Test User", email="test@test.com", password="Test password")
