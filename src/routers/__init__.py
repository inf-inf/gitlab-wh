from fastapi import APIRouter

from .api import api_router
from .pages import pages_router

main_router = APIRouter()
main_router.include_router(api_router)
main_router.include_router(pages_router)
