
import logging
from collections.abc import Callable, Coroutine
from traceback import format_exc
from typing import Any, NotRequired, TypedDict

from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse, Response
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR

from src import config

from .exceptions import RedirectError
from .templates import CommonTemplateResponseGenerator

logger = logging.getLogger("gitlab-wh.error")


class DebugFields(TypedDict):
    """Параметры для отображения дополнительной информации на странице ошибки"""
    traceback: str


class ErrorPageDefaultFields(TypedDict):
    """Параметры для страницы ошибки по умолчанию"""
    error_title: str
    error_message: str


class ErrorPageFields(ErrorPageDefaultFields):
    """Параметры для отображения страницы ошибки"""
    error_code: int
    debug: NotRequired[DebugFields]


error_messages: dict[int, ErrorPageDefaultFields] = {
    HTTP_404_NOT_FOUND: {
        "error_title": "Страница не найдена",
        "error_message": "В адресе есть ошибка или страница удалена.",
    },
    HTTP_422_UNPROCESSABLE_ENTITY: {
        "error_title": "Ошибка валидации",
        "error_message": "Проверьте отправляемые данные.",
    },
    HTTP_500_INTERNAL_SERVER_ERROR: {
        "error_title": "Ошибка сервера",
        "error_message": "Попробуйте обновить страницу позже.",
    },
}

default_error_message: ErrorPageDefaultFields = {
    "error_title": "Что-то пошло не так",
    "error_message": "Попробуйте обновить страницу позже.",
}


async def get_html_error_page(request: Request,
                              status_code: int,
                              error_title: str | None = None,
                              error_message: str | None = None,
                              ) -> Response:
    """Сгенерировать HTML страницу ошибки"""
    ctrg = CommonTemplateResponseGenerator(request, "pages/common")

    # Работаем с одним context для уменьшения нагрузки в рантайме
    context: ErrorPageFields = error_messages.get(status_code, default_error_message)   # type: ignore[assignment]
    context["error_code"] = status_code

    if error_title:
        context["error_title"] = error_title

    if error_message:
        context["error_message"] = error_message

    if config.SHOW_TRACEBACK:
        context["debug"] = {"traceback": format_exc()}


    return ctrg.generate_response("error.html.j2", context=context, status_code=status_code)



async def html_http_exception_handler(request: Request, exc: HTTPException) -> Response:
    """Обработчик ошибки HTTPException"""
    logger.exception("Ошибка HTTPException")

    if request.url.path.startswith("/api"):
        return await http_exception_handler(request, exc)

    error_message = exc.detail if exc.status_code != HTTP_404_NOT_FOUND else None

    return await get_html_error_page(request=request, status_code=exc.status_code, error_message=error_message)


async def html_request_validation_exception_handler(request: Request, exc: RequestValidationError) -> Response:
    """Обработчик ошибки RequestValidationError"""
    logger.exception("Ошибка RequestValidationError")

    if request.url.path.startswith("/api"):
        return await request_validation_exception_handler(request, exc)

    return await get_html_error_page(request=request, status_code=422)


async def html_unhandled_exception_handler(request: Request, _exc: Exception) -> Response:
    """Обработчик ошибки Exception"""
    logger.exception("Необработанная ошибка")

    if request.url.path.startswith("/api"):
        return PlainTextResponse("Internal Server Error", status_code=500)

    return await get_html_error_page(request=request, status_code=500)


async def redirect_exception_handler(_request: Request, exc: RedirectError) -> Response:
    """Обработчик ошибки Exception"""
    logger.exception("Ошибка RedirectError")

    return RedirectResponse(url=exc.url, status_code=exc.status_code)


exception_handlers: dict[int | type[Exception], Callable[[Request, Any], Coroutine[Any, Any, Response]]] = {
    RedirectError: redirect_exception_handler,
    HTTPException: html_http_exception_handler,
    RequestValidationError: html_request_validation_exception_handler,
    Exception: html_unhandled_exception_handler,
}
