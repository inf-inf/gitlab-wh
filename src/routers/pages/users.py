from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

users_router = APIRouter(prefix="/users", tags=["users"])
# TODO должно быть вынесено в отдельный класс + dependency
templates = Jinja2Templates(directory="src/templates")


@users_router.get("/sign_in", response_class=HTMLResponse, summary="Страница входа")
async def sign_in(request: Request) -> Any:
    """Страница входа в админ панель"""
    return templates.TemplateResponse("pages/users/sign_in.html.j2", {"request": request})
