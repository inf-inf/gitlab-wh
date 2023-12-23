from typing import Literal, NamedTuple


class Alert(NamedTuple):
    """Параметры уведомления для пользователя на странице

    level: Уровень уведомления. В зависимости от этого параметра выставляется цвет и иконка уведомления
    msg: Текст сообщения, которое будет выведено пользователю

    Элемент: /src/templates/elements/alert.html.j2
    """
    level: Literal["info", "success", "warning", "error"]
    msg: str
