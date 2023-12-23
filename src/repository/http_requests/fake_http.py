from types import TracebackType
from typing import Any, Generic, TypeVar

from aiohttp import ClientSession

T = TypeVar("T")


class FakeResponse(Generic[T]):
    """Mock Response object"""
    def __init__(self,
                 data: T | None = None,
                 status_code: int = 200,
                 headers: dict[str, str] | None = None,
                 ) -> None:
        """Конструктор

        Args:
            data: данные, которые вернутся в методе .json()
            status_code: статус код, который вернется при вызове атрибута .status
            headers: HTTP заголовки, которые вернутся при вызове атрибута .headers
        """
        self.data = data
        self.headers = headers or {}
        self.status_code = status_code

    async def __aenter__(self) -> "FakeResponse[T]":
        """Mock реализация __aenter__"""
        return self

    async def __aexit__(self,
                        exc_type: type[BaseException] | None,
                        exc_val: BaseException | None,
                        exc_tb: TracebackType | None,
                        ) -> None:
        """Mock реализация __aexit__"""

    async def json(self) -> T | None:
        """Mock реализация await *.json"""
        return self.data


class FakeClientSession(ClientSession):
    """Fake реализация aiohttp-сессии"""
    def __init__(self,
                 data: T | None = None,
                 status_code: int = 200,
                 headers: dict[str, str] | None = None,
                 ) -> None:
        """Конструктор

        Args:
            data: данные, которые вернутся в методе FakeResponse.json()
            status: статус код, который вернется при вызове атрибута FakeResponse.status
            headers: HTTP заголовки, которые вернутся при вызове атрибута FakeResponse.headers
        """
        self._fake_response = FakeResponse(data, status_code, headers)

    def fake_request(self, _url: str, *_args: Any, **_kwargs: Any) -> FakeResponse[Any]:
        """Mock ClientSession.get"""
        return self._fake_response

    get = fake_request  # type: ignore[assignment]
    post = fake_request  # type: ignore[assignment]
    put = fake_request  # type: ignore[assignment]
    patch = fake_request  # type: ignore[assignment]
    delete = fake_request  # type: ignore[assignment]
