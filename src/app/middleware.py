import http
import logging
from urllib.parse import quote

from starlette.types import ASGIApp, Message, Receive, Scope, Send

logger = logging.getLogger("gitlab-wh.access")
logger.setLevel(logging.INFO)

class AccessLogMiddleware:
    """Логирование запросов

    Данный Middleware осуществляет простой access log, для того чтобы выводить в терминал записи о запросах.
    Он необходим при использовании granian, тк он не логирует самостоятельно.
    При использовании, например, uvicorn, надобность в этом мидлвейре отпадет.
    """
    def __init__(self, app: ASGIApp) -> None:
        """Инициализация мидлвейра"""
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Обработка запроса"""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        client_addr = self._get_client_addr(scope)
        full_path = self._get_path_with_query_string(scope)
        protocol = f"HTTP/{scope['http_version']}"
        method = scope["method"]
        full_request_line = f"{method} {full_path} {protocol}"

        status_code = -1
        async def send_save_status(message: Message) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, send_save_status)
        except Exception:
            status_code = 500
            raise
        finally:
            level = self._get_level_by_status_code(status_code)
            status_phrase = http.HTTPStatus(status_code).phrase
            msg = f'{client_addr} - "{full_request_line}" {status_code} {status_phrase}'
            logger.log(level=level, msg=msg)

    @staticmethod
    def _get_client_addr(scope: Scope) -> str:
        if scope["client"] is None:
            return "-"
        return f"{scope['client'][0]}:{scope['client'][1]}"


    @staticmethod
    def _get_path_with_query_string(scope: Scope) -> str:
        """Получить полный путь запроса, включая Query параметры"""
        path_with_query_string = quote(scope.get("root_path", "") + scope["path"])
        if scope["query_string"]:
            return f"{path_with_query_string}?{scope['query_string'].decode('ascii')}"
        return path_with_query_string

    @staticmethod
    def _get_level_by_status_code(status_code: int) -> int:
        """Выбор loglevel в зависимости от статуса ответа.

        Возможно, стоит отказаться от этого и логировать все с logging.INFO
        """
        return logging.ERROR if status_code >= 500 else logging.WARNING if 500 > status_code >= 400 else logging.INFO
