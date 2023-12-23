from typing import Any

import pytest


@pytest.fixture()
def request_data() -> dict[str, Any]:
    """Возвращает данные для FakeClientSession.fake_request"""
    data = {"some": "data"}
    headers = {"some": "headers"}
    status_code = 333
    return {
        "data": data,
        "headers": headers,
        "status_code": status_code,
    }
