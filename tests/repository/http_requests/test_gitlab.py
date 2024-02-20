from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar
from uuid import uuid4

import pytest
from aiohttp import ClientSession

from src.repository.http_requests.fake_http import FakeClientSession
from src.repository.http_requests.gitlab import GitLabHTTPv4

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


class TestGitLabHTTP:
    """Testing class GitLabHTTP"""
    test_check_data: ClassVar[list[tuple[dict[str, Any], bool]]] = [
        (
            {
                "data": [{"some": "value"}],
                "status": 200,
            },
            True,
        ),
        (
            {
                "data": {"some": "value"},
                "status": 200,
            },
            False,
        ),
        (
            {
                "data": [{"some": "value"}],
                "status": 400,
            },
            False,
        ),
        (
            {
                "data": {"some": "value"},
                "status": 500,
            },
            False,
        ),
    ]

    @pytest.mark.parametrize(("response_from_gitlab", "expected"), test_check_data)
    @pytest.mark.asyncio()
    async def test_check(self,
                         response_from_gitlab: dict[str, Any],
                         expected: bool,  # noqa: FBT001
                         ) -> None:
        """Testing GitLabHTTP.check"""
        fake_client_session = FakeClientSession(**response_from_gitlab)
        gitlab_http = GitLabHTTPv4(fake_client_session)
        assert await gitlab_http.check() is expected


@pytest.mark.integration()
@pytest.mark.asyncio()
class TestIntegrationGitLabHTTP:
    """Integration testing class GitLabHTTP"""

    async def _create_new_gitlab_http(self, personal_access_token: str) -> AsyncGenerator[GitLabHTTPv4, None]:
        """Возвращает новый экземпляр GitLabHTTPv4 с PRIVATE-TOKEN == personal_access_token"""
        headers = {"PRIVATE-TOKEN": personal_access_token}
        async with ClientSession("http://localhost", headers=headers) as client_session:
            yield GitLabHTTPv4(client_session)

    async def test_create_project(self, root_client_session: ClientSession) -> None:
        """Testing GitLabHTTP.create_project"""
        gitlab_http = GitLabHTTPv4(root_client_session)

        project_name = project_path = str(uuid4())
        project_id = await gitlab_http.create_project(project_name, project_path)

        projects = await gitlab_http.list_projects()
        assert project_id in (project["id"] for project in projects)

    async def test_create_group(self, root_client_session: ClientSession) -> None:
        """Testing GitLabHTTP.create_group"""
        gitlab_http = GitLabHTTPv4(root_client_session)

        group_name = group_path = str(uuid4())
        group_id = await gitlab_http.create_group(group_name, group_path)

        groups = await gitlab_http.list_groups()
        assert group_id in (group["id"] for group in groups)

    async def test_create_subgroup(self, root_client_session: ClientSession) -> None:
        """Testing GitLabHTTP.create_subgroup"""
        gitlab_http = GitLabHTTPv4(root_client_session)

        group_name = group_path = str(uuid4())
        parent_group_id = await gitlab_http.create_group(group_name, group_path)

        subgroup_id = await gitlab_http.create_subgroup("subgroup", "subgroup", parent_group_id)

        parent_group, subgroup = await gitlab_http.list_groups(search=group_name, order_by="id")
        assert parent_group["id"] == parent_group_id
        assert parent_group["parent_id"] is None
        assert subgroup["id"] == subgroup_id
        assert subgroup["parent_id"] == parent_group_id
        assert subgroup["full_path"] == f"{group_name}/subgroup"

    async def test_create_user(self, root_client_session: ClientSession) -> None:
        """Testing GitLabHTTP.create_user"""
        gitlab_http = GitLabHTTPv4(root_client_session)

        user_name = user_username = str(uuid4())
        some_uuid_password = str(uuid4())
        email = user_username + "@example.com"
        user_id = await gitlab_http.create_user(user_name, user_username, email, some_uuid_password)

        user_from_gitlab = await gitlab_http.get_user(user_id)
        assert user_id == user_from_gitlab["id"]
        assert user_username == user_from_gitlab["username"]
        assert user_name == user_from_gitlab["name"]

    async def test_create_personal_access_token(self, root_client_session: ClientSession) -> None:
        """Testing GitLabHTTP.create_personal_access_token"""
        gitlab_http = GitLabHTTPv4(root_client_session)

        user_name = user_username = access_token_name = str(uuid4())
        some_uuid_password = str(uuid4())
        email = user_username + "@example.com"
        user_id = await gitlab_http.create_user(user_name, user_username, email, some_uuid_password)

        personal_access_token = await gitlab_http.create_personal_access_token(user_id, access_token_name, ["api"])

        _gen_gitlab_http = self._create_new_gitlab_http(personal_access_token)
        new_gitlab_http = await anext(_gen_gitlab_http)
        users_personal_access_tokens = await new_gitlab_http.list_personal_access_tokens(search=access_token_name)
        assert len(users_personal_access_tokens) == 1
        assert users_personal_access_tokens[0]["name"] == access_token_name

    async def test_add_user_to_group(self, root_client_session: ClientSession) -> None:
        """Testing GitLabHTTP.add_user_to_group"""
        gitlab_http = GitLabHTTPv4(root_client_session)

        user_name = user_username = str(uuid4())
        some_uuid_password = str(uuid4())
        email = user_username + "@example.com"
        user_id = await gitlab_http.create_user(user_name, user_username, email, some_uuid_password)

        group_name = group_path = str(uuid4())
        group_id = await gitlab_http.create_group(group_name, group_path)

        await gitlab_http.add_user_to_group(group_id, user_id, 40)

        group_members = await gitlab_http.list_group_members(group_id, user_ids=[user_id])
        assert user_id == group_members[0]["id"]

    async def test_add_user_to_project(self, root_client_session: ClientSession) -> None:
        """Testing GitLabHTTP.add_user_to_project"""
        gitlab_http = GitLabHTTPv4(root_client_session)

        user_name = user_username = str(uuid4())
        some_uuid_password = str(uuid4())
        email = user_username + "@example.com"
        user_id = await gitlab_http.create_user(user_name, user_username, email, some_uuid_password)

        project_name = project_path = str(uuid4())
        project_id = await gitlab_http.create_project(project_name, project_path)

        await gitlab_http.add_user_to_project(project_id, user_id, 40)

        project_members = await gitlab_http.list_project_members(project_id, user_ids=[user_id])
        assert user_id == project_members[0]["id"]
