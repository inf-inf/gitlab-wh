from collections.abc import Callable
from pathlib import Path

from fastapi import Request

from src.app.templates import CommonTemplateResponseGenerator


def get_common_trg(request: Request) -> CommonTemplateResponseGenerator:
    """Инициализировать генератор CommonTemplateResponseGenerator"""
    return CommonTemplateResponseGenerator(request)


def get_common_trg_prefill_path(directory: str | Path = "") -> Callable[[Request], CommonTemplateResponseGenerator]:
    """Инициализировать генератор CommonTemplateResponseGenerator с предзаполненим пути до директории шаблона"""

    def get_common_trg(request: Request) -> CommonTemplateResponseGenerator:
        return CommonTemplateResponseGenerator(request, directory)

    return get_common_trg
