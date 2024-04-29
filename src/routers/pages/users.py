"""deprecated

Изначальная идея была в заведении учеток пользователей, к которым крепились бы токены доступа.
Однако, решено было упростить пользовательский путь. В данный момент используется форма авторизации сразу по токену
из GitLab в роутере index
"""
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Query, Response
from fastapi.responses import HTMLResponse

from src.app.templates import CommonTemplateResponseGenerator
from src.dependencies.templates import get_common_trg_prefill_path
from src.models.pages.alert import Alert

users_router = APIRouter(prefix="/users", tags=["pages.users"], deprecated=True)

GetTRGDep = Annotated[CommonTemplateResponseGenerator, Depends(get_common_trg_prefill_path("pages/users"))]


@users_router.get("/sign_in", response_class=HTMLResponse, summary="Страница входа")
async def get_sign_in(get_trg: GetTRGDep,
                      redirect: str = Query("/", description=("Страница, на которую произойдет редирект в случае "
                                                              "успешной авторизации")),
                      ) -> Response:
    """Страница входа в админ панель"""
    context = {
          "redirect": redirect,
    }
    return get_trg.generate_response("sign_in.html.j2", context)

@users_router.post("/sign_in", summary="Обработка авторизации")
async def post_sign_in(get_trg: GetTRGDep,
                       username: str = Form(min_length=1, max_length=20, description="Имя пользователя"),
                       password: str = Form(min_length=1, max_length=20, description="Пароль"),  # noqa: ARG001
                       redirect: str = Form("/", description=("Страница, на которую произойдет редирект в случае "
                                                              "успешной авторизации")),
                       ) -> Response:
      """Авторизация, проверка логина и пароля"""
      context = {
            "username": username,
            "redirect": redirect,
      }
      alert = Alert(level="error", msg="Неверный логин или пароль")
      return get_trg.generate_response("sign_in.html.j2", context=context, alert=alert)
