from fastapi import APIRouter

index_router = APIRouter(tags=["index"])


@index_router.get("/", summary="Главная страница")
async def index() -> None:
    """Главная страница"""
    return
