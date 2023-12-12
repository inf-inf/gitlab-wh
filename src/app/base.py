from typing import Any

from fastapi import APIRouter, FastAPI


class GitLabWH(FastAPI):
    """Приложение GitLab-WH"""
    def __init__(self, *, main_router: APIRouter, **kwargs: Any):
        """Конструктор

        :param main_router: основной роутер приложения, в который стекаются все остальные роутеры
        """
        super().__init__(**kwargs)
        self.include_router(main_router)
