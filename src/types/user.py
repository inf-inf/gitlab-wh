from datetime import datetime
from typing import Literal, TypedDict

AccessLevel = Literal[0, 5, 10, 20, 30, 40, 50]


class _User(TypedDict):
    """Модель описывающая пользователя в GitLab

    Args:
        id: идентификатор пользователя
        username: никнейм пользователя
        name: имя пользователя
        state: статус пользователя (активен, неактивен и т.п.)
        locked: заблокирован ли пользователь (True - заблокирован)
        avatar_url: URL адрес для получения аватара пользователя
        web_url: URL адрес страницы пользователя
        created_at: время создания пользователя (с timezone)

    Example:
        {
            "id": 87,
            "username": "ksqroow",
            "name": "Dima Dima",
            "state": "active",
            "locked": False,
            "avatar_url": "https://www.gravatar.com/avatar/dd4012c1bd3544d6dad51235899c593a?s=80&d=identicon",
            "web_url": "http://localhost/ksqroow",
            "created_at": "2024-02-15T22:02:11.623Z"
        }
    """
    id: int
    username: str
    name: str
    state: str
    locked: bool
    avatar_url: str
    web_url: str
    created_at: datetime


class CreatedUser(_User):
    """Модель пользователя GitLab непосредственно после его создания

    Example:
        {
            "id": 84,
            "username": "60f4e2b9-4c0a-4e8f-81e6-bf3cd940f937",
            "name": "60f4e2b9-4c0a-4e8f-81e6-bf3cd940f937",
            "state": "active",
            "locked": False,
            "avatar_url": "https://www.gravatar.com/avatar/44d7564971ab53b409a6e2911c22446a?s=80&d=identicon",
            "web_url": "http://localhost/60f4e2b9-4c0a-4e8f-81e6-bf3cd940f937",
            "created_at": "2024-02-15T21:48:16.403Z",
            "bio": "",
            "location": "",
            "public_email": None,
            "skype": "",
            "linkedin": "",
            "twitter": "",
            "discord": "",
            "website_url": "",
            "organization": "",
            "job_title": "",
            "pronouns": None,
            "bot": False,
            "work_information": None,
            "followers": 0,
            "following": 0,
            "is_followed": False,
            "local_time": None,
            "last_sign_in_at": None,
            "confirmed_at": None,
            "last_activity_on": None,
            "email": "60f4e2b9-4c0a-4e8f-81e6-bf3cd940f937@example.com",
            "theme_id": 3,
            "color_scheme_id": 1,
            "projects_limit": 100000,
            "current_sign_in_at": None,
            "identities": [],
            "can_create_group": True,
            "can_create_project": True,
            "two_factor_enabled": False,
            "external": False,
            "private_profile": False,
            "commit_email": "60f4e2b9-4c0a-4e8f-81e6-bf3cd940f937@example.com",
            "shared_runners_minutes_limit": None,
            "extra_shared_runners_minutes_limit": None,
            "scim_identities": [],
            "is_admin": False,
            "note": None,
            "namespace_id": 238,
            "created_by": {
                "id": 1,
                "username": "root",
                "name": "Administrator",
                "state": "active",
                "locked": False,
                "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
                "web_url": "http://localhost/root"
            },
            "using_license_seat": False
        }
    """


class GetUserByAdmin(_User):
    """Модель пользователя GitLab при просмотре с правами администратора

    Example:
        {
            "id": 87,
            "username": "ksqroow",
            "name": "Dima Dima",
            "state": "active",
            "locked": False,
            "avatar_url": "https://www.gravatar.com/avatar/dd4012c1bd3544d6dad51235899c593a?s=80&d=identicon",
            "web_url": "http://localhost/ksqroow",
            "created_at": "2024-02-15T22:02:11.623Z",
            "bio": "",
            "location": "",
            "public_email": None,
            "skype": "",
            "linkedin": "",
            "twitter": "",
            "discord": "",
            "website_url": "",
            "organization": "",
            "job_title": "",
            "pronouns": None,
            "bot": False,
            "work_information": None,
            "followers": 0,
            "following": 0,
            "is_followed": False,
            "local_time": None,
            "last_sign_in_at": "2024-02-15T22:03:13.692Z",
            "confirmed_at": "2024-02-15T22:02:11.543Z",
            "last_activity_on": "2024-02-15",
            "email": "qwe@qwe.ru",
            "theme_id": 3,
            "color_scheme_id": 1,
            "projects_limit": 100000,
            "current_sign_in_at": "2024-02-15T22:03:13.692Z",
            "identities": [],
            "can_create_group": True,
            "can_create_project": True,
            "two_factor_enabled": False,
            "external": False,
            "private_profile": False,
            "commit_email": "qwe@qwe.ru",
            "shared_runners_minutes_limit": None,
            "extra_shared_runners_minutes_limit": None,
            "scim_identities": [],
            "is_admin": False,
            "note": None,
            "namespace_id": 243,
            "created_by": None,
            "using_license_seat": False,
            "highest_role": 0,
            "current_sign_in_ip": "172.17.0.1",
            "last_sign_in_ip": "172.17.0.1",
            "sign_in_count": 1,
            "plan": None,
            "trial": False
        }
    """


class GetUser(_User):
    """Модель пользователя GitLab при просмотре под обычным пользователем

    Example:
        {
            "id": 87,
            "username": "ksqroow",
            "name": "Dima Dima",
            "state": "active",
            "locked": False,
            "avatar_url": "https://www.gravatar.com/avatar/dd4012c1bd3544d6dad51235899c593a?s=80&d=identicon",
            "web_url": "http://localhost/ksqroow",
            "created_at": "2024-02-15T22:02:11.623Z",
            "bio": "",
            "location": "",
            "public_email": None,
            "skype": "",
            "linkedin": "",
            "twitter": "",
            "discord": "",
            "website_url": "",
            "organization": "",
            "job_title": "",
            "pronouns": None,
            "bot": False,
            "work_information": None,
            "local_time": None
        }
    """


class AddUserToProjectOrGroup(_User):
    """Модель пользователя GitLab при добавлении пользователя к репозиторию или к группе

    Example:
        {
            "access_level": 40,
            "created_at": "2024-02-15T21:48:55.182Z",
            "created_by": {
                "id": 1,
                "username": "root",
                "name": "Administrator",
                "state": "active",
                "locked": False,
                "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
                "web_url": "http://localhost/root"
            },
            "expires_at": None,
            "id": 84,
            "username": "60f4e2b9-4c0a-4e8f-81e6-bf3cd940f937",
            "name": "60f4e2b9-4c0a-4e8f-81e6-bf3cd940f937",
            "state": "active",
            "locked": False,
            "avatar_url": "https://www.gravatar.com/avatar/44d7564971ab53b409a6e2911c22446a?s=80&d=identicon",
            "web_url": "http://localhost/60f4e2b9-4c0a-4e8f-81e6-bf3cd940f937",
            "membership_state": "active"
        }
    """


class GetCurrentUser(_User):
    """Модель пользователя GitLab при запросе данных о самом себе (когда ты обычный пользователь)

    Example:
        {
            "id": 87,
            "username": "ksqroow",
            "name": "Dima Dima",
            "state": "active",
            "locked": False,
            "avatar_url": "https://www.gravatar.com/avatar/dd4012c1bd3544d6dad51235899c593a?s=80&d=identicon",
            "web_url": "http://localhost/ksqroow",
            "created_at": "2024-02-15T22:02:11.623Z",
            "bio": "",
            "location": "",
            "public_email": None,
            "skype": "",
            "linkedin": "",
            "twitter": "",
            "discord": "",
            "website_url": "",
            "organization": "",
            "job_title": "",
            "pronouns": None,
            "bot": False,
            "work_information": None,
            "local_time": None,
            "last_sign_in_at": "2024-02-15T22:03:13.692Z",
            "confirmed_at": "2024-02-15T22:02:11.543Z",
            "last_activity_on": "2024-02-15",
            "email": "qwe@qwe.ru",
            "theme_id": 3,
            "color_scheme_id": 1,
            "projects_limit": 100000,
            "current_sign_in_at": "2024-02-15T22:03:13.692Z",
            "identities": [],
            "can_create_group": True,
            "can_create_project": True,
            "two_factor_enabled": False,
            "external": False,
            "private_profile": False,
            "commit_email": "qwe@qwe.ru",
            "shared_runners_minutes_limit": None,
            "extra_shared_runners_minutes_limit": None,
            "scim_identities": []
        }
    """


class GetCurrentUserByAdmin(_User):
    """Модель пользователя GitLab при запросе данных о самом себе (когда ты администратор)

    Example:
        {
            "id": 1,
            "username": "root",
            "name": "Administrator",
            "state": "active",
            "locked": False,
            "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
            "web_url": "http://localhost/root",
            "created_at": "2024-01-18T21:50:28.016Z",
            "bio": "",
            "location": "",
            "public_email": None,
            "skype": "",
            "linkedin": "",
            "twitter": "",
            "discord": "",
            "website_url": "",
            "organization": "",
            "job_title": "",
            "pronouns": None,
            "bot": False,
            "work_information": None,
            "local_time": None,
            "last_sign_in_at": "2024-02-03T22:45:06.333Z",
            "confirmed_at": "2024-01-18T21:50:27.830Z",
            "last_activity_on": "2024-02-15",
            "email": "admin@example.com",
            "theme_id": 3,
            "color_scheme_id": 1,
            "projects_limit": 100000,
            "current_sign_in_at": "2024-02-15T22:02:20.181Z",
            "identities": [],
            "can_create_group": True,
            "can_create_project": True,
            "two_factor_enabled": False,
            "external": False,
            "private_profile": False,
            "commit_email": "admin@example.com",
            "shared_runners_minutes_limit": None,
            "extra_shared_runners_minutes_limit": None,
            "scim_identities": [],
            "is_admin": True,
            "note": None,
            "namespace_id": 1,
            "created_by": None,
            "using_license_seat": False
        }
    """


class MemberUser(_User):
    """Модель пользователя, которая возвращается при запросе членов группы/репозитория

    Args:
        access_level: уровень доступа пользователя к репозиторию/группе

    Example:
        {
            "access_level": 40,
            "created_at": "2024-02-18T14:26:04.939Z",
            "created_by": {
                "id": 1,
                "username": "root",
                "name": "Administrator",
                "state": "active",
                "locked": False,
                "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
                "web_url": "http://localhost/root"
            },
            "expires_at": None,
            "id": 89,
            "username": "577c4f44-c0a5-437f-8e01-839d8ff434f1",
            "name": "577c4f44-c0a5-437f-8e01-839d8ff434f1",
            "state": "active",
            "locked": False,
            "avatar_url": "https://www.gravatar.com/avatar/22aaddc681e315f460b0cea77f912385?s=80&d=identicon",
            "web_url": "http://localhost/577c4f44-c0a5-437f-8e01-839d8ff434f1",
            "membership_state": "active"
        }
    """
    access_level: AccessLevel
