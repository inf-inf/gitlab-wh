from typing import Any


class BaseHTTP:
    """Базовый класс для реализации HTTP запросов"""
    def __init__(self) -> None:
        """Конструктор"""
        self._session = ...

    async def _get(self,
                   url: str,
                   params: dict[str, Any] | None = None,
                   headers: dict[str, Any] | None = None
                   ) -> dict[str, Any]:
        """Реализация GET запроса

        Args:
            url: URL-адрес для GET запроса
            params: словарь ключей и их значений для GET запроса
            headers: заголовки для GET запроса

        Returns:
            Результат GET запроса (JSON в виде словаря)
        """
        return {}

    async def _post(self,
                    url: str,
                    data: dict[str, Any] | None = None,
                    headers: dict[str, Any] | None = None
                    ) -> dict[str, Any]:
        """Реализация POST запроса

        Args:
            url: URL-адрес для POST запроса
            data: тело для POST запроса
            headers: заголовки для POST запроса

        Returns:
            Результат POST запроса (JSON в виде словаря)
        """
        return {}

    async def _put(self,
                   url: str,
                   data: dict[str, Any] | None = None,
                   headers: dict[str, Any] | None = None
                   ) -> dict[str, Any]:
        """Реализация PUT запроса

        Args:
            url: URL-адрес для PUT запроса
            data: тело для PUT запроса
            headers: заголовки для PUT запроса

        Returns:
            Результат PUT запроса (JSON в виде словаря)
        """
        return {}

    async def _patch(self,
                     url: str,
                     data: dict[str, Any] | None = None,
                     headers: dict[str, Any] | None = None
                     ) -> dict[str, Any]:
        """Реализация PATCH запроса

        Args:
            url: URL-адрес для PATCH запроса
            data: тело для PATCH запроса
            headers: заголовки для PATCH запроса

        Returns:
            Результат PATCH запроса (JSON в виде словаря)
        """
        return {}

    async def _delete(self,
                      url: str,
                      params: dict[str, Any] | None = None,
                      headers: dict[str, Any] | None = None
                      ) -> dict[str, Any]:
        """Реализация DELETE запроса

        Args:
            url: URL-адрес для DELETE запроса
            params: словарь ключей и их значений для DELETE запроса
            headers: заголовки для DELETE запроса

        Returns:
            Результат DELETE запроса (JSON в виде словаря)
        """
        return {}
