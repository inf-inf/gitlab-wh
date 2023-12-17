from fastapi import APIRouter

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/sign_in", summary="Страница входа")
async def sign_in() -> None:
    """Страница входа в админ панель"""
    return
