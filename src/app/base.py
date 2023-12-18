from typing import Any

from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

from src import config


class GitLabWH(FastAPI):
    """Приложение GitLab-WH"""

    config = config

    def __init__(self, *, main_router: APIRouter, **kwargs: Any):
        """Конструктор

        :param main_router: основной роутер приложения, в который стекаются все остальные роутеры
        """
        super().__init__(**kwargs)
        self.include_router(main_router)
        self.mount("/static", StaticFiles(directory=self.config.STATIC_FOLDER_PATH), name="static")
