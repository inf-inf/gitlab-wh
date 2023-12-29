import logging

import colorlog
from fastapi import FastAPI

from . import config
from .app import GitLabWH
from .routers import main_router

handler = logging.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        fmt="%(asctime)s - %(purple)s%(name)s%(reset)s - %(log_color)s%(levelname)s%(reset)s - %(message)s",
    ),
)
logging.basicConfig(level=logging.INFO, handlers=[handler])

gitlab_wh = GitLabWH(
    app_type=FastAPI,
    main_router=main_router,
    static_folder_path=config.STATIC_FOLDER_PATH,
)
