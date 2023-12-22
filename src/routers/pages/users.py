from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response
from fastapi.responses import HTMLResponse

from src.app.templates import CommonTemplateResponseGenerator
from src.dependencies.templates import get_common_trg_prefill_path

users_router = APIRouter(prefix="/users", tags=["pages.users"])

GetTRGDep = Annotated[CommonTemplateResponseGenerator, Depends(get_common_trg_prefill_path("pages/users"))]


@users_router.get("/sign_in", response_class=HTMLResponse, summary="Страница входа")
async def sign_in(get_trg: GetTRGDep,
                  redirect: str = Query("/", description=("Страница, на которую произойдет редирект в случае "
                                                          "успешной авторизации")),
                  ) -> Response:
    """Страница входа в админ панель"""
    context = {
          "redirect": redirect,
    }
    return get_trg.generate_response("sign_in.html.j2", context)
