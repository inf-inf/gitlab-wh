from fastapi import APIRouter

from .index import index_router
from .users import users_router

pages_router = APIRouter()
pages_router.include_router(index_router)
pages_router.include_router(users_router)
