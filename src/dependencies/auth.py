import urllib.parse

from fastapi import Depends, Request
from fastapi.security import APIKeyCookie

from src.app.exceptions import RedirectError

cookie_scheme = APIKeyCookie(name="auth_token", description="Токен сессии клиента", auto_error=False)

def get_auth_token(request: Request, auth_token: str | None = Depends(cookie_scheme)) -> str:
    """Проверка авторизации

    Args:
        request (Request): Контекст запроса
        auth_token (str | None, optional): Токен сессии (ввв данный момент personal access token)

    Returns:
        str: personal access token
    """
    # TODO поменять на токен сессии, возвращать модель для работы с сессией,
    # TODO из которой можно будет получать personal access token и др из бд
    if not auth_token:
        params = {
            "warning": "Необходимо пройти авторизацию",
            "redirect": request.url.path,
        }
        query = urllib.parse.urlencode(params)
        raise RedirectError(url=f"/sign_in?{query}")

    # TODO проверка на правильность токена
    return auth_token
