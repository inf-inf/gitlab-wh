from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import RedirectResponse

from src.app.templates import CommonTemplateResponseGenerator
from src.dependencies.templates import get_common_trg_prefill_path

index_router = APIRouter(tags=["pages.index"])

GetTRGDep = Annotated[CommonTemplateResponseGenerator, Depends(get_common_trg_prefill_path("pages/common"))]


@index_router.get("/", summary="Главная страница")
async def index(get_trg: GetTRGDep) -> Response:
    """Главная страница"""
    return get_trg.generate_response("index.html.j2")

@index_router.get("/favicon.ico", summary="Редирект фавикон", response_class=RedirectResponse)
async def redirect_favicon() -> RedirectResponse:
    """В случае если на странице не указан адрес фавикона, средиректить браузер"""
    return RedirectResponse(url="/static/img/favicon.png", status_code=status.HTTP_301_MOVED_PERMANENTLY)
