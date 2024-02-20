from __future__ import annotations

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

    async def list_groups(self, min_access_level: AccessLevel = 10) -> list[GroupModel]:
        """Получение списка всех доступных групп, к которым уровень доступа не меньше min_access_level

        Args:
            min_access_level: уровень доступа

        Returns:
            список групп, удовлетворяющих условию, что уровень доступа к ним >= чем min_access_level
        """
        params = {"min_access_level": min_access_level}
        response: ResponseModel[list[GroupModel]] = await self._get(self.URL_GROUPS, params)
        if response.status_code == HTTPStatus.OK:
            return response.data
        raise GitLabError(response.data)

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
