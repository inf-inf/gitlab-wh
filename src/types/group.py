from typing import Literal, TypedDict

GroupsOrderBy = Literal["name", "path", "id", "similarity"]


class Group(TypedDict):
    """Модель описывающая группу в GitLab

    Args:
        id: идентификатор группы
        full_path: полный путь до группы
        parent_id: идентификатор родительской группы (если ее нет, то None)

    Example:
        {
            "id": 106,
            "web_url": "http://localhost/groups/02886886-4bb0-4785-85db-95f65641d7f8",
            "name": "02886886-4bb0-4785-85db-95f65641d7f8",
            "path": "02886886-4bb0-4785-85db-95f65641d7f8",
            "description": "",
            "visibility": "private",
            "share_with_group_lock": False,
            "require_two_factor_authentication": False,
            "two_factor_grace_period": 48,
            "project_creation_level": "developer",
            "auto_devops_enabled": None,
            "subgroup_creation_level": "maintainer",
            "emails_disabled": False,
            "emails_enabled": True,
            "mentions_disabled": None,
            "lfs_enabled": True,
            "default_branch_protection": 2,
            "default_branch_protection_defaults": {},
            "avatar_url": None,
            "request_access_enabled": True,
            "full_name": "02886886-4bb0-4785-85db-95f65641d7f8",
            "full_path": "02886886-4bb0-4785-85db-95f65641d7f8",
            "created_at": "2024-01-28T14:11:50.818Z",
            "parent_id": None,
            "shared_runners_setting": "enabled",
            "ldap_cn": None,
            "ldap_access": None,
            "wiki_access_level": "enabled"
        }
    """
    id: int
    full_path: str
    parent_id: int | None
