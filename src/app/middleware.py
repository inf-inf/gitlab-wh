import http
import logging
import time
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

        start_time = time.time()
        try:
            await self.app(scope, receive, send_save_status)
        except Exception:
            status_code = 500
            raise
        finally:
            end_time = time.time()
            duration_ms = int((end_time - start_time) * 1_000)
            status_phrase = http.HTTPStatus(status_code).phrase
            logger.info(
                '"%(full_request_line)s" %(status_code)s %(status_phrase)s (%(duration_ms)s мс)',
                {
                    "full_request_line": full_request_line,
                    "status_code": status_code,
                    "status_phrase": status_phrase,
                    "duration_ms": duration_ms,
                },
            )


    @staticmethod
    def _get_path_with_query_string(scope: Scope) -> str:
        """Получить полный путь запроса, включая Query параметры"""
        path_with_query_string = quote(scope.get("root_path", "") + scope["path"])
        if scope["query_string"]:
            return f"{path_with_query_string}?{scope['query_string'].decode('ascii')}"
        return path_with_query_string
