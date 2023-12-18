from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.responses import HTMLResponse

from src.app.templates import CommonTemplateResponseGenerator
from src.dependencies.templates import get_common_trg_prefill_path

users_router = APIRouter(prefix="/users", tags=["users"])

get_trg_dep = Annotated[CommonTemplateResponseGenerator, Depends(get_common_trg_prefill_path("pages/users"))]


@users_router.get("/sign_in", response_class=HTMLResponse, summary="Страница входа")
async def sign_in(get_trg: get_trg_dep) -> Response:
    """Страница входа в админ панель"""
    return get_trg.generate_response("sign_in.html.j2")
