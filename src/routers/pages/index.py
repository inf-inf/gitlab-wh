from typing import Annotated

from fastapi import APIRouter, Depends, Form, Query, Response, status
from fastapi.responses import RedirectResponse

from src.app.templates import CommonTemplateResponseGenerator
from src.dependencies.auth import get_auth_token
from src.dependencies.templates import get_common_trg_prefill_path
from src.models.pages.alert import Alert

index_router = APIRouter(tags=["pages.index"])

GetTRGDep = Annotated[CommonTemplateResponseGenerator, Depends(get_common_trg_prefill_path("pages/common"))]


@index_router.get("/", summary="Главная страница")
async def index(get_trg: GetTRGDep, _auth_token: str = Depends(get_auth_token)) -> Response:
    """Главная страница"""
    return get_trg.generate_response("index.html.j2")

@index_router.get("/favicon.ico", summary="Редирект фавикон", response_class=RedirectResponse)
async def redirect_favicon() -> RedirectResponse:
    """В случае если на странице не указан адрес фавикона, средиректить браузер"""
    return RedirectResponse(url="/static/img/favicon.ico", status_code=status.HTTP_301_MOVED_PERMANENTLY)

@index_router.get("/sign_in", summary="Страница входа")
async def get_sign_in(get_trg: GetTRGDep,
                      redirect: str = Query("/", description=("Страница, на которую произойдет редирект в случае "
                                                              "успешной авторизации")),
                      warning: str | None = Query(None, description="Предупреждение"),
                      ) -> Response:
    """Страница входа в админ панель"""
    context = {
          "redirect": redirect,
    }
    alert = Alert(level="warning", msg=warning) if warning else None
    return get_trg.generate_response("sign_in.html.j2", context, alert=alert)

@index_router.post("/sign_in", summary="Обработка авторизации")
async def post_sign_in(get_trg: GetTRGDep,
                       access_token: str = Form(min_length=1, max_length=255,
                                                description="Personal Access Token пользователя/бота"),
                       redirect: str = Form("/", description=("Страница, на которую произойдет редирект в случае "
                                                              "успешной авторизации")),
                       ) -> Response:
    """Авторизация, проверка логина и пароля"""
    # TODO проверка токена
    if access_token == "12345":  # noqa: S105
        context = {
            "access_token": access_token,
            "redirect": redirect,
        }
        alert = Alert(level="error", msg="Неверный токен")
        return get_trg.generate_response("sign_in.html.j2", context=context, alert=alert)

    response = RedirectResponse(url=redirect, status_code=302)
    response.set_cookie(key="auth_token", value=access_token)
    return response
