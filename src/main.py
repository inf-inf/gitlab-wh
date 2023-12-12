from .app import GitLabWH
from .routers import main_router

gitlab_wh = GitLabWH(main_router=main_router)
