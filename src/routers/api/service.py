from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

service_router = APIRouter(prefix="/service", tags=["api.service"])


@service_router.get("/ping", summary="Проверка доступности API")
async def ping() -> PlainTextResponse:
    """Метод проверки доступности API

    Должен отвечать `pong` при доступности и работоспособности приложения
    """
    return PlainTextResponse("pong")


from aiohttp import ClientSession

from src.repository.http_requests.gitlab import GitLabHTTPv4


@service_router.get("/debug", summary="Проверка доступности API")
async def debug() -> PlainTextResponse:
    """Метод проверки доступности API

    Должен отвечать `pong` при доступности и работоспособности приложения
    """
    async with ClientSession("http://localhost", headers={"PRIVATE-TOKEN": "test-token-123"}) as session:
        gitlab_http = GitLabHTTPv4(session)
        return await gitlab_http.create_group("cool", "cool")
