from pathlib import Path

from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles


class GitLabWH:
    """Приложение GitLab-WH"""

    def __init__(self, app_type: type[FastAPI], main_router: APIRouter, static_folder_path: Path) -> None:
        """Конструктор приложения"""
        self._app = app_type()
        self._app.include_router(main_router)
        self._app.mount("/static", StaticFiles(directory=static_folder_path), name="static")

    @property
    def app(self) -> FastAPI:
        """FastAPI приложение"""
        return self._app
