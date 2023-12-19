from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse

index_router = APIRouter(tags=["index"])


@index_router.get("/", summary="Главная страница")
async def index() -> None:
    """Главная страница"""
    return

@index_router.get("/favicon.ico", summary="Редирект фавикон", response_class=RedirectResponse)
async def redirect_favicon() -> RedirectResponse:
    """В случае если на странице не указан адрес фавикона, средиректить браузер"""
    return RedirectResponse(url="/static/img/favicon.png", status_code=status.HTTP_301_MOVED_PERMANENTLY)
