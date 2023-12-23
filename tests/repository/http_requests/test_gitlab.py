from typing import Any, ClassVar

import pytest

from src.repository.http_requests.gitlab import GitLabHTTP
from tests.repository.mocks import FakeClientSession


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
