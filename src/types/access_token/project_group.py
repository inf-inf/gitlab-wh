from .access_token import AccessToken


class ProjectGroupAccessToken(AccessToken):
    """Модель описывающая Project/Group Access Token в GitLab

    Args:
        access_level: уровень доступа к репозиторию/группе

    Example:
        {
            "id": 65,
            "name": "e274f270-8469-463d-888f-5fabf0e6ecf1",
            "revoked": False,
            "created_at": "2024-02-12T20:17:07.913Z",
            "scopes": ["api"],
            "user_id": 80,
            "active": True,
            "expires_at": "2025-02-10",
            "access_level": 30
        }
    """
    access_level: int


class CreatedProjectGroupAccessToken(ProjectGroupAccessToken):
    """Модель описывающая Project/Group Access Token в GitLab в момент его создания

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
            "active": True,
            "expires_at": "2025-02-10",
            "access_level": 30
            "token": "glpat-rwN5ixF7RyzLhn4w-FuD"
        }
    """
    token: str
