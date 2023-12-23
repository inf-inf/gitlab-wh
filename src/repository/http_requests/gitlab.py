from http import HTTPStatus

from .base import BaseHTTP


class GitLabHTTP(BaseHTTP):
    """Запросы в GitLab API"""
    PING = "/api/v4/projects"

    async def check(self) -> bool:
        """Проверка доступности GitLab API"""
        response = await self._get(self.PING)
        return response.status_code == HTTPStatus.OK and isinstance(response.data, list)
