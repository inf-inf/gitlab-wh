import os
from collections.abc import AsyncGenerator
from typing import Any

import pytest
from aiohttp import ClientSession


@pytest.fixture()
async def root_client_session() -> AsyncGenerator[ClientSession, None]:
    """Возвращает ClientSession с PRIVATE-TOKEN от root пользователя"""
    headers = {"PRIVATE-TOKEN": os.environ["ROOT_PERSONAL_ACCESS_TOKEN"]}
    async with ClientSession("http://localhost", headers=headers) as client_session:
        yield client_session


@pytest.fixture()
def request_data() -> dict[str, Any]:
    """Возвращает данные для FakeClientSession.fake_request"""
    data = {"some": "data"}
    headers = {"some": "headers"}
    status = 333
    return {
        "data": data,
        "headers": headers,
        "status": status,
    }
