from pathlib import Path
from typing import Any

from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles


class GitLabWH(FastAPI):
    """Приложение GitLab-WH"""

    CURRENT_PATH = Path(__file__).absolute().parent.parent
    STATIC_FOLDER_PATH = Path(CURRENT_PATH, "static")

    def __init__(self, *, main_router: APIRouter, **kwargs: Any):
        """Конструктор

        :param main_router: основной роутер приложения, в который стекаются все остальные роутеры
        """
        super().__init__(**kwargs)
        self.include_router(main_router)
        self.mount("/static", StaticFiles(directory=self.STATIC_FOLDER_PATH), name="static")
