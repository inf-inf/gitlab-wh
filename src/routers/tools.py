from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

tools_router = APIRouter(prefix="/tools")


@tools_router.get("/ping")
async def ping() -> PlainTextResponse:
    """Метод проверки доступности API"""
    return PlainTextResponse("PONG")
