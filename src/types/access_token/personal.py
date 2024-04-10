from datetime import datetime

from .access_token import AccessToken


class PersonalAccessToken(AccessToken):
    """Модель описывающая Personal Access Token в GitLab

    Args:
        last_used_at: дата и время последнего использования токена (с timezone)

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
    last_used_at: datetime


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
