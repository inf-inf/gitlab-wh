from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


def test_ping(client: TestClient) -> None:
    """Test /tools/ping"""
    response = client.get("/tools/ping")
    assert response.text == "PONG"
