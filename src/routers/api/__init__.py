from fastapi import APIRouter

from .service import service_router

api_router = APIRouter(prefix="/api")
api_router.include_router(service_router)
