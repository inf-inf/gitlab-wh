from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse

pages_service_router = APIRouter(tags=["pages.service"])


@pages_service_router.get("/favicon.ico", summary="Редирект фавикон", response_class=RedirectResponse)
async def redirect_favicon() -> RedirectResponse:
    """В случае если на странице не указан адрес фавикона, средиректить браузер"""
    return RedirectResponse(url="/static/img/favicon.ico", status_code=status.HTTP_301_MOVED_PERMANENTLY)
