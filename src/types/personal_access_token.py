from datetime import date, datetime
from typing import Literal, TypedDict

# https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#personal-access-token-scopes
AccessTokenScopes = Literal["api", "read_user", "read_api", "read_repository", "write_repository", "read_registry",
                            "write_registry", "sudo", "admin_mode", "create_runner", "ai_features", "k8s_proxy",
                            "read_service_ping"]


class PersonalAccessToken(TypedDict):
    """Модель описывающая Personal Access Token в GitLab

    Args:
        id: идентификатор токена авторизации
        name: наименование токена авторизации
        revoked: признак того, что токен был отозван (то есть больше не работает)
        created_at: дата и время создания токена (с timezone)
        scopes: список разрешенных действий для токена
        user_id: идентификатор пользователя, которому принадлежит токен
        last_used_at: дата и время последнего использования токена (с timezone)
        active: признак того, что токен сейчас используется (активен)
        expires_at: дата, когда токен будет заблокирован

    Example:
        {
            "id": 67,
            "name": "22c0f4c4-6dd5-45f6-87b8-6212f347169f",
            "revoked": False,
            "created_at": "2024-02-12T21:08:03.671Z",
            "scopes": ["api"],
            "user_id": 83,
            "last_used_at": "2024-02-12T21:09:39.864Z",
            "active": True,
            "expires_at": "2025-02-11"
        }
    """
    id: int
    name: str
    revoked: bool
    created_at: datetime
    scopes: list[AccessTokenScopes]
    user_id: int
    last_used_at: datetime
    active: bool
    expires_at: date | None


class CreatedPersonalAccessToken(PersonalAccessToken):
    """Модель описывающая Personal Access Token в GitLab в момент его создания

    Args:
        token: созданный токен

    Example:
        {
            "id": 65,
            "name": "e274f270-8469-463d-888f-5fabf0e6ecf1",
            "revoked": False,
            "created_at": "2024-02-12T20:17:07.913Z",
            "scopes": ["api"],
            "user_id": 80,
            "last_used_at": None,
            "active": True,
            "expires_at": "2025-02-10",
            "token": "glpat-rwN5ixF7RyzLhn4w-FuD"
        }
    """
    token: str
