from datetime import date, datetime
from typing import Literal, TypedDict

# https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#personal-access-token-scopes
AccessTokenScopes = Literal["api", "read_user", "read_api", "read_repository", "write_repository", "read_registry",
                            "write_registry", "sudo", "admin_mode", "create_runner", "ai_features", "k8s_proxy",
                            "read_service_ping"]


class AccessToken(TypedDict):
    """Модель описывающая Access Token в GitLab

    Args:
        id: идентификатор токена авторизации
        name: наименование токена авторизации
        revoked: признак того, что токен был отозван (то есть больше не работает)
        created_at: дата и время создания токена (с timezone)
        scopes: список разрешенных действий для токена
        user_id: идентификатор пользователя, которому принадлежит токен
        active: признак того, что токен сейчас используется (активен)
        expires_at: дата, когда токен будет заблокирован
    """
    id: int
    name: str
    revoked: bool
    created_at: datetime
    scopes: list[AccessTokenScopes]
    user_id: int
    active: bool
    expires_at: date | None
