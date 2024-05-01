from pathlib import Path

from fastapi import APIRouter, FastAPI
from fastapi.middleware import Middleware
from fastapi.staticfiles import StaticFiles

from .exception_handlers import exception_handlers
from .middleware import AccessLogMiddleware


class GitLabWH:
    """Приложение GitLab-WH"""

    def __init__(self, app_type: type[FastAPI], main_router: APIRouter, static_folder_path: Path) -> None:
        """Конструктор приложения"""
        self._app = app_type(
            title="GitLab-WH",
            openapi_url="/api/service/openapi.json",
            openapi_tags=sorted([
                {
                    "name": "api.service",
                    "description": "Сервисные методы API",
                },
                {
                    "name": "pages.index",
                    "description": "Основные страницы",
                },
                {
                    "name": "pages.users",
                    "description": "Страницы для работы с учетной записью пользователя",
                },
                {
                    "name": "pages.service",
                    "description": "Сервисные методы фронта",
                },
            ], key=lambda tag: tag["name"]),
            swagger_ui_parameters={
                "displayRequestDuration": True,
                "filter": True,
                "requestSnippetsEnabled": True,
            },
            exception_handlers=exception_handlers,
            middleware=[Middleware(AccessLogMiddleware)],
        )
        self._app.include_router(main_router)
        self._app.mount("/static", StaticFiles(directory=static_folder_path), name="static")

    @property
    def app(self) -> FastAPI:
        """FastAPI приложение"""
        return self._app
