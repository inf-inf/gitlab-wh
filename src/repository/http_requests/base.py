from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, TypeVar

if TYPE_CHECKING:
    from collections.abc import Mapping

    from aiohttp import ClientSession


T = TypeVar("T")


@dataclass
class ResponseModel(Generic[T]):
    """Модель Response, возвращаемая BaseHTTP

    Args:
        data: тело HTTP ответа
        status_code: статус код HTTP ответа
        headers: заголовки HTTP ответа
    """
    data: T
    status_code: int
    headers: Mapping[str, str]


class BaseHTTP:
    """Базовый класс для реализации HTTP запросов"""
    def __init__(self, session: ClientSession) -> None:
        """Конструктор"""
        self._session = session

    async def _get(self,
                   url: str,
                   params: dict[str, Any] | None = None,
                   headers: dict[str, Any] | None = None,
                   ) -> ResponseModel[Any]:
        """Реализация GET запроса

        Args:
            url: URL-адрес для GET запроса
            params: словарь ключей и их значений для GET запроса
            headers: заголовки для GET запроса

        Returns:
            Результат GET запроса (JSON в виде словаря)
        """
        async with self._session.get(url, params=params, headers=headers) as response:
            return ResponseModel(
                data=await response.json(),
                status_code=response.status,
                headers=response.headers,
            )

    async def _post(self,
                    url: str,
                    data: dict[str, Any],
                    headers: dict[str, Any] | None = None,
                    ) -> ResponseModel[Any]:
        """Реализация POST запроса

        Args:
            url: URL-адрес для POST запроса
            data: тело для POST запроса
            headers: заголовки для POST запроса

        Returns:
            Результат POST запроса (JSON в виде словаря)
        """
        async with self._session.post(url, json=data, headers=headers) as response:
            return ResponseModel(
                data=await response.json(),
                status_code=response.status,
                headers=response.headers,
            )

    async def _put(self,
                   url: str,
                   data: dict[str, Any],
                   headers: dict[str, Any] | None = None,
                   ) -> ResponseModel[Any]:
        """Реализация PUT запроса

        Args:
            url: URL-адрес для PUT запроса
            data: тело для PUT запроса
            headers: заголовки для PUT запроса

        Returns:
            Результат PUT запроса (JSON в виде словаря)
        """
        async with self._session.put(url, json=data, headers=headers) as response:
            return ResponseModel(
                data=await response.json(),
                status_code=response.status,
                headers=response.headers,
            )

    async def _patch(self,
                     url: str,
                     data: dict[str, Any],
                     headers: dict[str, Any] | None = None,
                     ) -> ResponseModel[Any]:
        """Реализация PATCH запроса

        Args:
            url: URL-адрес для PATCH запроса
            data: тело для PATCH запроса
            headers: заголовки для PATCH запроса

        Returns:
            Результат PATCH запроса (JSON в виде словаря)
        """
        async with self._session.patch(url, json=data, headers=headers) as response:
            return ResponseModel(
                data=await response.json(),
                status_code=response.status,
                headers=response.headers,
            )

    async def _delete(self,
                      url: str,
                      params: dict[str, Any] | None = None,
                      headers: dict[str, Any] | None = None,
                      ) -> ResponseModel[Any]:
        """Реализация DELETE запроса

        Args:
            url: URL-адрес для DELETE запроса
            params: словарь ключей и их значений для DELETE запроса
            headers: заголовки для DELETE запроса

        Returns:
            Результат DELETE запроса (JSON в виде словаря)
        """
        async with self._session.delete(url, params=params, headers=headers) as response:
            return ResponseModel(
                data=await response.json(),
                status_code=response.status,
                headers=response.headers,
            )
