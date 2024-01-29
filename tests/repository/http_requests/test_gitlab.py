from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar
from uuid import uuid4

import pytest

from src.repository.http_requests.fake_http import FakeClientSession
from src.repository.http_requests.gitlab import GitLabHTTP

if TYPE_CHECKING:
    from aiohttp import ClientSession


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
        gitlab_http = GitLabHTTP(fake_client_session)
        assert await gitlab_http.check() is expected


class TestIntegrationGitLabHTTP:
    """Integration testing class GitLabHTTP"""
    @pytest.mark.asyncio()
    @pytest.mark.integration()
    async def test_create_group(self, root_client_session: ClientSession) -> None:
        """Testing GitLabHTTP.create_group"""
        some_uuid = str(uuid4())
        gitlab_http = GitLabHTTP(root_client_session)
        group_id = await gitlab_http.create_group(some_uuid, some_uuid)
        groups = await gitlab_http.list_groups()
        assert group_id in (group["id"] for group in groups)
