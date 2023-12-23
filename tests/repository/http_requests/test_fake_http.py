from typing import Any

import pytest

from src.repository.http_requests.fake_http import FakeClientSession, FakeResponse


class TestFakeResponse:
    """Testing class FakeResponse"""

    @pytest.mark.asyncio()
    async def test_aenter(self) -> None:
        """Testing FakeResponse.__aenter__"""
        async with FakeResponse() as fake_response:
            assert isinstance(fake_response, FakeResponse)

    @pytest.mark.asyncio()
    async def test_json(self) -> None:
        """Testing FakeResponse.json"""
        data = {"some": "data"}
        fake_response = FakeResponse(data=data)
        assert await fake_response.json() == data


class TestFakeClientSession:
    """Testing class FakeClientSession"""

    def test_fake_request(self, request_data: dict[str, Any]) -> None:
        """Testing FakeClientSession.fake_request"""
        fake_client_session = FakeClientSession(**request_data)
        fake_response = fake_client_session.fake_request("http://some_url")
        assert isinstance(fake_response, FakeResponse)
        assert fake_response.data == request_data["data"]
        assert fake_response.headers == request_data["headers"]
        assert fake_response.status == request_data["status_code"]

    def test_get(self, request_data: dict[str, Any]) -> None:
        """Testing FakeClientSession.get"""
        self.test_fake_request(request_data)

    def test_post(self, request_data: dict[str, Any]) -> None:
        """Testing FakeClientSession.post"""
        self.test_fake_request(request_data)

    def test_put(self, request_data: dict[str, Any]) -> None:
        """Testing FakeClientSession.put"""
        self.test_fake_request(request_data)

    def test_patch(self, request_data: dict[str, Any]) -> None:
        """Testing FakeClientSession.patch"""
        self.test_fake_request(request_data)

    def test_delete(self, request_data: dict[str, Any]) -> None:
        """Testing FakeClientSession.delete"""
        self.test_fake_request(request_data)
