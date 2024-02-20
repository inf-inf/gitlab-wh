from __future__ import annotations

import asyncio
from datetime import date, timedelta
from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from .base import BaseHTTP, ResponseModel

if TYPE_CHECKING:
    from src.types import Sort, State
    from src.types.group import Group, GroupsOrderBy
    from src.types.personal_access_token import AccessTokenScopes, CreatedPersonalAccessToken, PersonalAccessToken
    from src.types.project import CreatedProject, Project, ProjectsOrderBy
    from src.types.user import (
        AccessLevel,
        AddUserToProjectOrGroup,
        CreatedUser,
        GetCurrentUser,
        GetCurrentUserByAdmin,
        GetUser,
        GetUserByAdmin,
        MemberUser,
    )


class GitLabError(Exception):
    """Базовый exception для GitLabHTTP"""


class GitLabHTTPv4(BaseHTTP):
    """Запросы в GitLab API"""
    URL_ADD_USER_TO_GROUP = "/api/v4/groups/{group_id}/members"
    URL_ADD_USER_TO_PROJECT = "/api/v4/projects/{project_id}/members"
    URL_GROUPS = "/api/v4/groups"
    URL_PROJECTS = "/api/v4/projects"
    URL_PING = URL_PROJECTS
    URL_USER = "/api/v4/user"
    URL_USERS = "/api/v4/users"
    URL_CURRENT_USER = URL_USER
    URL_PERSONAL_ACCESS_TOKEN = "/api/v4/users/{user_id}/personal_access_tokens"  # noqa: S105
    URL_ALL_PERSONAL_ACCESS_TOKEN = "/api/v4/personal_access_tokens"  # noqa: S105
    URL_GROUP_MEMBERS = URL_ADD_USER_TO_GROUP
    URL_PROJECT_MEMBERS = URL_ADD_USER_TO_PROJECT

    async def _offset_pagination(self,
                                 url: str,
                                 params: dict[str, Any],
                                 headers: dict[str, Any] | None = None,
                                 *,
                                 page: int,
                                 ) -> list[dict[str, Any]]:
        """GET запрос для пагинации с использованием offset'ов

        GitLab offset-based pagination - https://docs.gitlab.com/ee/api/rest/index.html#offset-based-pagination

        Args:
            url: URL-адрес для GET запроса
            params: словарь ключей и их значений для GET запроса
            headers: заголовки для GET запроса
            page: номер следующей возвращаемой страницы

        Returns:
            Тело ответа на один GET запрос
        """
        params["page"] = page
        async with self._session.get(url, params=params, headers=headers) as response:
            res: list[dict[str, Any]] = await response.json()
            return res

    async def _by_pagination(self,
                             url: str,
                             params: dict[str, Any] | None = None,
                             headers: dict[str, Any] | None = None,
                             ) -> ResponseModel[Any]:
        """Получение всех записей (множество GET запросов) с использованием пагинаций

        GitLab paginations - https://docs.gitlab.com/ee/api/rest/index.html#pagination

        Args:
            url: URL-адрес для GET запроса
            params: словарь ключей и их значений для GET запроса
            headers: заголовки для GET запроса

        Returns:
            Агрегированный результат множества GET запросов (агрегация пагинаций),
            где статус код и заголовки будут от самого 1-го запроса в пачке
        """
        params = params or {}
        params["per_page"] = 100
        params["page"] = 1

        first_response = await self._get_one(url, params, headers)

        total_pages = first_response.headers["X-Total-Pages"]
        tasks = [self._offset_pagination(url, params, headers, page=page) for page in range(2, int(total_pages) + 1)]
        results = await asyncio.gather(*tasks)
        return ResponseModel(
            data=sum(results, first_response.data),
            status_code=first_response.status_code,
            headers=first_response.headers,
        )

    async def check(self) -> bool:
        """Проверка доступности GitLab API

        Returns:
            True - GitLab доступен, False - GitLab недоступен
        """
        response = await self._get(self.URL_PING)
        return response.status_code == HTTPStatus.OK and isinstance(response.data, list)

    async def add_user_to_group(self,
                                group_id: int,
                                user_id: int,
                                access_level: AccessLevel,
                                ) -> int:
        """Добавление пользователя к группе GitLab

        Args:
            group_id: идентификатор группы
            user_id: идентификатор пользователя
            access_level: уровень доступа

        Returns:
            идентификатор добавленного пользователя
        """
        url = self.URL_ADD_USER_TO_GROUP.format(group_id=group_id)
        return await self._add_user(url, user_id, access_level)

    async def add_user_to_project(self,
                                  project_id: int,
                                  user_id: int,
                                  access_level: AccessLevel,
                                  ) -> int:
        """Добавление пользователя к репозиторию GitLab

        Args:
            project_id: идентификатор репозитория
            user_id: идентификатор пользователя
            access_level: уровень доступа

        Returns:
            идентификатор добавленного пользователя
        """
        url = self.URL_ADD_USER_TO_PROJECT.format(project_id=project_id)
        return await self._add_user(url, user_id, access_level)

    async def create_group(self,
                           name: str,
                           path: str,
                           ) -> int:
        """Создание группы в GitLab

        Args:
            name: наименование новой группы
            path: путь до новой группы

        Returns:
            идентификатор созданной группы
        """
        return await self._create_group(name, path)

    async def create_subgroup(self,
                              name: str,
                              path: str,
                              parent_id: int,
                              ) -> int:
        """Создание подгруппы в GitLab

        Args:
            name: наименование новой подгруппы
            path: путь до новой подгруппы
            parent_id: идентификатор родительской группы

        Returns:
            идентификатор созданной подгруппы
        """
        return await self._create_group(name, path, parent_id)

    async def create_project(self,
                             name: str,
                             path: str,
                             *,
                             initialize_with_readme: bool = True,
                             only_allow_merge_if_all_discussions_are_resolved: bool = True,
                             only_allow_merge_if_pipeline_succeeds: bool = True,
                             ) -> int:
        """Создание репозитория в GitLab

        Args:
            name: наименование нового репозитория
            path: путь до нового репозитория
            initialize_with_readme: True - инициализировать репозиторий в README.md файлом, False - без README.md
            only_allow_merge_if_all_discussions_are_resolved: True - сливать MR можно только после разрешения
                всех discussion под MR, False - можно сливать MR и без разрешения всех discussion
            only_allow_merge_if_pipeline_succeeds: True - сливать MR можно только при success pipeline, False - можно
                сливать MR и при fail pipeline

        Returns:
            идентификатор созданного репозитория
        """
        data = {
            "name": name,
            "path": path,
            "initialize_with_readme": initialize_with_readme,
            "only_allow_merge_if_all_discussions_are_resolved": only_allow_merge_if_all_discussions_are_resolved,
            "only_allow_merge_if_pipeline_succeeds": only_allow_merge_if_pipeline_succeeds,
        }
        response: ResponseModel[ProjectModel] = await self._post(self.URL_PROJECTS, data)
        if response.status_code == HTTPStatus.CREATED:
            return response.data["id"]
        raise GitLabError(response.data)

    async def create_user(self,
                          name: str,
                          username: str,
                          email: str,
                          password: str,
                          ) -> int:
        """Создание пользователя в GitLab

        Args:
            name: имя нового пользователя
            username: псевдоним(nickname) нового пользователя
            email: почтовый адрес нового пользователя
            password: пароль для нового пользователя

        Returns:
            идентификатор созданного пользователя
        """
        data = {
            "name": name,
            "username": username,
            "email": email,
            "password": password,
        }
        response: ResponseModel[UserModel] = await self._post(self.URL_USERS, data)
        if response.status_code == HTTPStatus.CREATED:
            return response.data["id"]
        raise GitLabError(response.data)

    async def create_personal_access_token(self,
                                           user_id: int,
                                           name: str,
                                           scopes: list[AccessTokenScopes],
                                           expires_at: date | None = None,
                                           ) -> str:
        """Создание Personal Access Token для пользователя

        ВНИМАНИЕ! Только с токеном администратора (Admin token only)

        Create a personal access token - https://docs.gitlab.com/ee/api/users.html#create-a-personal-access-token

        Args:
            user_id: идентификатор пользователя
            name: наименование токена доступа
            scopes: список разрешенных действий для токена
            expires_at: время, когда токен истечет

        Returns:
            Созданный Personal Access Token для пользователя с id=user_id
        """
        url = self.URL_PERSONAL_ACCESS_TOKEN.format(user_id=user_id)
        data = {
            "name": name,
            "scopes": scopes,
            "expires_at": str(expires_at or date.today() + timedelta(days=364)),
        }
        response: ResponseModel[CreatedPersonalAccessToken] = await self._post(url, data)
        if response.status_code == HTTPStatus.CREATED:
            return response.data["token"]
        raise GitLabError(response.data)

    async def list_personal_access_tokens(self,
                                          search: str | None = None,
                                          revoked: bool | None = None,
                                          state: State | None = None,
                                          ) -> list[PersonalAccessToken]:
        """Получения списка всех Personal Access Token для пользователя

        List personal access tokens -
            https://docs.gitlab.com/ee/api/personal_access_tokens.html#list-personal-access-tokens

        Args:
            search: поле для фильтрации токена доступа (судя по всему фильтр используется по имени токена)
            revoked: True - найти только отозванные токены, False - найти все действующие токены
            state: состояние токена (активен или неактивен)

        Returns:
            Список объектов Personal Access Token для пользователя
        """
        params = {
            "search": search,
            "revoked": revoked,
            "state": state,
        }
        response: ResponseModel[list[PersonalAccessToken]] = await self._get(self.URL_ALL_PERSONAL_ACCESS_TOKEN,
                                                                             params,
                                                                             by_pagination=True)
        if response.status_code == HTTPStatus.OK:
            return response.data
        raise GitLabError(response.data)

    async def get_current_user(self) -> GetCurrentUser | GetCurrentUserByAdmin:
        """Получение информации по текущему пользователю

        List current user - https://docs.gitlab.com/ee/api/users.html#list-current-user

        Returns:
            Объект пользователя
        """
        # TODO: механизм корректного определения GetCurrentUser или GetCurrentUserByAdmin (без run-time проверки)
        response: ResponseModel[GetCurrentUser | GetCurrentUserByAdmin] = await self._get(self.URL_USER)
        if response.status_code == HTTPStatus.OK:
            return {
                "id": response.data["id"],
                "username": response.data["username"],
                "name": response.data["name"],
                "state": response.data["state"],
                "locked": response.data["locked"],
                "avatar_url": response.data["avatar_url"],
                "web_url": response.data["web_url"],
                "created_at": response.data["created_at"],
            }
        raise GitLabError(response.data)

    async def get_user(self, user_id: int) -> GetUser | GetUserByAdmin:
        """Получение пользователя

        Single user - https://docs.gitlab.com/ee/api/users.html#single-user
            For user - https://docs.gitlab.com/ee/api/users.html#for-user
            For admin - https://docs.gitlab.com/ee/api/users.html#for-administrators-1

        Args:
            user_id: идентификатор пользователя

        Returns:
            Объект пользователя
        """
        # TODO: механизм корректного определения GetUser или GetUserByAdmin (без run-time проверки)
        response: ResponseModel[GetUser | GetUserByAdmin] = await self._get(f"{self.URL_USERS}/{user_id}")
        if response.status_code == HTTPStatus.OK:
            return {
                "id": response.data["id"],
                "username": response.data["username"],
                "name": response.data["name"],
                "state": response.data["state"],
                "locked": response.data["locked"],
                "avatar_url": response.data["avatar_url"],
                "web_url": response.data["web_url"],
                "created_at": response.data["created_at"],
            }
        raise GitLabError(response.data)

    async def list_groups(self,
                          *,
                          search: str | None = None,
                          order_by: GroupsOrderBy = "name",
                          sort: Sort = "asc",
                          min_access_level: AccessLevel = 10,
                          ) -> list[Group]:
        """Получение списка всех доступных групп

        List groups - https://docs.gitlab.com/ee/api/groups.html#list-groups

        Args:
            search: поле для фильтрации групп (судя по всему фильтр используется по имени групп)
            order_by: признак, по которому будут отсортированы группы
            sort: сортировка по полю order_by должна быть asc или desc
            min_access_level: уровень доступа

        Returns:
            Список объектов группы
        """
        params = {
            "search": search,
            "order_by": order_by,
            "sort": sort,
            "min_access_level": min_access_level,
        }
        response: ResponseModel[list[Group]] = await self._get(self.URL_GROUPS, params, by_pagination=True)
        if response.status_code == HTTPStatus.OK:
            return response.data
        raise GitLabError(response.data)

    async def list_projects(self,
                            *,
                            order_by: ProjectsOrderBy = "created_at",
                            sort: Sort = "desc",
                            ) -> list[Project]:
        """Получение списка всех доступных репозиториев

        List all projects - https://docs.gitlab.com/ee/api/projects.html#list-all-projects

        Args:
            order_by: признак, по которому будут отсортированы репозитории
            sort: сортировка по полю order_by должна быть asc или desc

        Returns:
            Список объектов репозитория
        """
        params = {"order_by": order_by, "sort": sort}
        response: ResponseModel[list[Project]] = await self._get(self.URL_PROJECTS, params, by_pagination=True)
        if response.status_code == HTTPStatus.OK:
            return response.data
        raise GitLabError(response.data)

    async def list_group_members(self,
                                 group_id: int,
                                 *,
                                 query: str | None = None,
                                 user_ids: list[int] | None = None,
                                 skip_users: list[int] | None = None,
                                 ) -> list[MemberUser]:
        """Получение списка пользователей группы

        List all members of a group - https://docs.gitlab.com/ee/api/members.html#list-all-members-of-a-group-or-project

        Args:
            group_id: id группы GitLab, список пользователей которых хотим узнать
            query: поле для фильтрации пользователей (судя по всему фильтрация по username пользователя)
            user_ids: фильтрация пользователей, id которых есть среди user_ids
            skip_users: пропустить пользователей, id которых есть среди skip_users

        Returns:
            Список пользователей, которые принадлежат группе с group_id
        """
        url = self.URL_GROUP_MEMBERS.format(group_id=group_id)
        return await self._list_members(url, query=query, user_ids=user_ids, skip_users=skip_users)

    async def list_project_members(self,
                                   project_id: int,
                                   *,
                                   query: str | None = None,
                                   user_ids: list[int] | None = None,
                                   skip_users: list[int] | None = None,
                                   ) -> list[MemberUser]:
        """Получение списка пользователей репозитория

        List all members of a project -
            https://docs.gitlab.com/ee/api/members.html#list-all-members-of-a-group-or-project

        Args:
            project_id: id репозитория GitLab, список пользователей которого хотим узнать
            query: поле для фильтрации пользователей (судя по всему фильтрация по username пользователя)
            user_ids: фильтрация пользователей, id которых есть среди user_ids
            skip_users: пропустить пользователей, id которых есть среди skip_users

        Returns:
            Список пользователей, которые принадлежат репозиторию с project_id
        """
        url = self.URL_PROJECT_MEMBERS.format(project_id=project_id)
        return await self._list_members(url, query=query, user_ids=user_ids, skip_users=skip_users)

    async def _add_user(self,
                        url: str,
                        user_id: int,
                        access_level: AccessLevel,
                        ) -> int:
        """Добавление пользователя к группе/репозиторию в GitLab

        Args:
            url: сформированный url GitLab API для добавления пользователя к группе/репозиторию в GitLab
            user_id: идентификатор пользователя
            access_level: уровень доступа

        Returns:
            идентификатор добавленного пользователя
        """
        data = {
            "user_id": user_id,
            "access_level": access_level,
        }
        response: ResponseModel[UserModel] = await self._post(url, data)
        if response.status_code == HTTPStatus.CREATED:
            return response.data["id"]
        raise GitLabError(response.data)

    async def _create_group(self,
                            name: str,
                            path: str,
                            parent_id: int | None = None,
                            ) -> int:
        """Создание группы/подгруппы в GitLab

        Args:
            name: наименование новой группы/подгруппы
            path: путь до новой группы/подгруппы
            parent_id: идентификатор родительской группы (если создается подгруппа)

        Returns:
            идентификатор созданной группы/подгруппы
        """
        data = {
            "name": name,
            "path": path,
            "parent_id": parent_id,
        }
        response: ResponseModel[GroupModel] = await self._post(self.URL_GROUPS, data)
        if response.status_code == HTTPStatus.CREATED:
            return response.data["id"]
        raise GitLabError(response.data)

    async def _list_members(self,
                            url: str,
                            *,
                            query: str | None = None,
                            user_ids: list[int] | None = None,
                            skip_users: list[int] | None = None,
                            ) -> list[MemberUser]:
        """Получение списка пользователей репозитория/группы

        List all members of a group or project -
            https://docs.gitlab.com/ee/api/members.html#list-all-members-of-a-group-or-project

        Args:
            url: сформированный URL для запроса членов группы или репозитория
            query: поле для фильтрации пользователей (судя по всему фильтрация по username пользователя)
            user_ids: фильтрация пользователей, id которых есть среди user_ids
            skip_users: пропустить пользователей, id которых есть среди skip_users

        Returns:
            Список пользователей репозитория/группы
        """
        params = {
            "query": query,
            "user_ids": user_ids,
            "skip_users": skip_users,
        }
        response: ResponseModel[list[MemberUser]] = await self._get(url, params=params, by_pagination=True)
        if response.status_code == HTTPStatus.OK:
            return response.data
        raise GitLabError(response.data)
