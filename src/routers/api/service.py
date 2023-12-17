from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

service_router = APIRouter(prefix="/service", tags=["service"])


@service_router.get("/ping", summary="Проверка доступности API")
async def ping() -> PlainTextResponse:
    """Метод проверки доступности API

    Должен отвечать `pong` при доступности и работоспособности приложения
    """
    return PlainTextResponse("pong")
