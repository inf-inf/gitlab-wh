from collections.abc import Mapping
from pathlib import Path
from typing import Any

from fastapi import Request, Response
from fastapi.templating import Jinja2Templates
from starlette.background import BackgroundTask

from src import config
from src.models.pages.alert import Alert


class CommonTemplateResponseGenerator:
    """Модель для работы с Jinja2 шаблонами

    Реализует общую логику, необходимую для генерации HTML.
    Предзаполняет обязательный Request, и также префикс пути до папки с шаблоном.

    Базовая директория (`config.HTML_TEMPLATES_FOLDER_PATH`) должна быть статична и указывать
    на папку templates для предсказуемого разрешения импортов внутри шаблонов.

    Параметр `directory` в `self.__init__` конкатенируется с `name` в `self.generate_response`
    для упрощения работы с несколькими шаблонами в рамках одного роутера. Полученный путь
    учитывается относительно базовой папки templates. Эти параметры необязательны, и служат
    лишь для упрощения. Эквивалентно, можно указать полный путь сразу в `name` из `self.generate_response`.
    """
    _templates = Jinja2Templates(directory=config.HTML_TEMPLATES_FOLDER_PATH)

    def __init__(self, request: Request, directory: str | Path = "") -> None:
        """Конструктор модели. Сохраняет Request и префикс пути для предзаполнения

        Args:
            request (Request): контекст запроса FastAPI
            directory (str | Path, optional): необязательный префикс пути до шаблона (директория)
                относительно `config.HTML_TEMPLATES_FOLDER_PATH`
        """
        self._directory = directory
        self._context: dict[str, Any] = {"request": request}

    def generate_response(self,
                          name: str,
                          context: Mapping[str, Any] | None = None,
                          alert: Alert | None = None,
                          status_code: int = 200,
                          headers: Mapping[str, str] | None = None,
                          media_type: str | None = None,
                          background: BackgroundTask | None = None,
                          ) -> Response:
        """Сгенерировать Response по шаблону Jinja2

        Args:
            name (str): имя файла шаблона
            context (Mapping[str, Any] | None, optional): параметры для подставления в шаблон
            alert (Alert, optional): уведомление для пользователя
            status_code (int, optional): Статус код ответа
            headers (Mapping[str, str] | None, optional): Хедеры ответа
            media_type (str | None, optional): media_type ответа
            background (BackgroundTask | None, optional): BackgroundTask ответа

        Returns:
            Response: фактически, HTMLResponse, готовая страница
        """
        template_name = Path(self._directory, name)

        if context:
            self._context.update(context)

        if alert:
            self._context.update({"alert": alert})

        return self._templates.TemplateResponse(
            name=str(template_name),
            context=self._context,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )
