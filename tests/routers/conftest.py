import pytest
from fastapi.testclient import TestClient

from src.main import gitlab_wh


@pytest.fixture()
def client() -> TestClient:
    """Возвращает экземпляр приложения FastAPI для тестирования"""
    return TestClient(gitlab_wh.app)
