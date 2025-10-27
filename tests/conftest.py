"""Configuración global de tests."""

from typing import Iterator  # noqa: UP035

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def test_app() -> FastAPI:
    """Fixture para el cliente de pruebas de FastAPI."""
    return app


@pytest.fixture
def client(test_app: FastAPI) -> Iterator[TestClient]:
    """Cliente de prueba para cada test"""
    with TestClient(test_app) as c:
        yield c
