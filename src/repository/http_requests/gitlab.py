from typing import ClassVar

from .base import BaseHTTP


class GitLabHTTP(BaseHTTP):
    """Запросы в GitLab API"""
    URLS: ClassVar[dict[str, str]] = {
        "ping": "/api/v4/projects",
    }

    async def check(self) -> bool:
        """Проверка доступности GitLab API"""
        response = await self._get(self.URLS["ping"])
        return response.status_code == 200 and isinstance(response.data, list)
