from fastapi import APIRouter

from .tools import tools_router

main_router = APIRouter()
main_router.include_router(tools_router)
