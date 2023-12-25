
from collections.abc import Callable, Coroutine
from typing import Any

from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.status import HTTP_404_NOT_FOUND

from .templates import CommonTemplateResponseGenerator


async def html_http_exception_handler(request: Request, exc: HTTPException) -> Response:
    """Обработчик ошибки HTTPException"""
    if request.url.path.startswith("/api"):
        return await http_exception_handler(request, exc)

    ctrg = CommonTemplateResponseGenerator(request, "pages/errors")

    if exc.status_code == HTTP_404_NOT_FOUND:
        return ctrg.generate_response("404.html.j2")

    context = {"error_code": exc.status_code, "error_message": exc.detail}
    return ctrg.generate_response("4xx.html.j2", context=context)


async def html_request_validation_exception_handler(request: Request, exc: RequestValidationError) -> Response:
    """Обработчик ошибки RequestValidationError"""
    if request.url.path.startswith("/api"):
        return await request_validation_exception_handler(request, exc)

    ctrg = CommonTemplateResponseGenerator(request, "pages/errors")
    return ctrg.generate_response("422.html.j2")


async def html_unhandled_exception_handler(request: Request, exc: Exception) -> Response:
    """Обработчик ошибки Exception"""
    if request.url.path.startswith("/api"):
        return PlainTextResponse("Internal Server Error", status_code=500)

    ctrg = CommonTemplateResponseGenerator(request, "pages/errors")
    return ctrg.generate_response("500.html.j2")


exception_handlers: dict[int | type[Exception], Callable[[Request, Any], Coroutine[Any, Any, Response]]] = {
    HTTPException: html_http_exception_handler,
    RequestValidationError: html_request_validation_exception_handler,
    Exception: html_unhandled_exception_handler,
}
