import asyncio
import logging
import os
import re
from collections.abc import AsyncGenerator, Generator
from typing import Any, Literal

import aiohttp

Action = Literal[
    # pull_request
    "assigned",
    "unassigned",
    "labeled",
    "unlabeled",
    "opened",
    "edited",
    "closed",
    "reopened",
    "synchronize",
    "converted_to_draft",
    "locked",
    "unlocked",
    "enqueued",
    "dequeued",
    "milestoned",
    "demilestoned",
    "ready_for_review",
    "review_requested",
    "review_request_removed",
    "auto_merge_enabled",
    "auto_merge_disabled",

    # pull_request_review
    "submitted",
    "dismissed",
    "edited",
]

State = Literal[
    "",  # if action is pull_request
    "approved",
    "commented",
    "dismissed",
]

QUERY_ISSUE_BY_PR = """
{
    repository(name: "{repo_name}", owner: "{repo_owner}") {
        pullRequest(number: {pull_request_id}) {
            closingIssuesReferences(first: 100) {
                totalCount
                nodes {
                    id
                    title
                    number
                    projectItems(first: 100) {
                        nodes {
                            id
                            fieldValueByName(name: "Status") {
                                ... on ProjectV2ItemFieldSingleSelectValue {
                                    id
                                    name
                                    optionId
                                }
                            }
                            project {
                                id
                                field(name: "Status") {
                                    ... on ProjectV2SingleSelectField {
                                        id
                                        name
                                        options {
                                            id
                                            name
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
"""

MUTATION_UPDATE_PROJECT_ITEM = """
mutation {
    updateProjectV2ItemFieldValue(
        input: {
            projectId: "{project_hash_id}",
            itemId: "{item_hash_id}",
            fieldId: "{field_hash_id}",
            value: {
                singleSelectOptionId : "{field_value_hash_id}"
            }
        }
    ) {
        clientMutationId
    }
}
"""


async def create_client_session(auth_token: str) -> AsyncGenerator[aiohttp.ClientSession, None]:
    """Создает aiohttp.ClientSession

    Args:
        auth_token: авторизационный токен к GitHub API

    """
    headers = {"Authorization": f"Bearer {auth_token}"}
    async with aiohttp.ClientSession(headers=headers) as session:
        yield session


async def graphql_request(client_session: aiohttp.ClientSession,
                          graphql_url: str,
                          query: str,
                          ) -> dict[str, Any]:
    """Запрос в GraphQL API

    Args:
        client_session: aiohttp сессия для HTTP запросов
        graphql_url: GitHub GraphQL API URL
        query: GraphQL запрос

    Returns:
        Ответ GitHub API на запрос
    """
    data = {"query": query}
    async with client_session.post(graphql_url, json=data) as response:
        resp_json: dict[str, Any] = await response.json()
        logging.info(resp_json)
        return resp_json


def generate_query(query_template: str, data: dict[str, str]) -> str:
    """Собирается query-запрос для GraphQL

    Args:
        query_template: шаблон для query-запроса
        data: key-value объект для заполнения шаблона query-запроса

    Returns:
        Сформированный query-запрос для GraphQL
    """
    query = re.sub(r"{repo_name}", data["repo_name"], query_template)
    query = re.sub(r"{repo_owner}", data["repo_owner"], query)
    return re.sub(r"{pull_request_id}", data["pull_request_id"], query)


def generate_mutation(mutatation_template: str, data: dict[str, Any]) -> str:
    """Собирается mutation-запрос для GraphQL

    Args:
        mutatation_template: шаблон для mutatation-запроса
        data: словарь с данными для для заполнения шаблона mutation-запроса

    Returns:
        Сформированный mutatation-запрос для GraphQL
    """
    mutation = re.sub(r"{project_hash_id}", data["project_hash_id"], mutatation_template)
    mutation = re.sub(r"{item_hash_id}", data["item_hash_id"], mutation)
    mutation = re.sub(r"{field_hash_id}", data["field_hash_id"], mutation)
    return re.sub(r"{field_value_hash_id}", data["field_value_hash_id"], mutation)


def parse_query_results(data: dict[str, Any]) -> Generator[dict[str, Any], None, None]:
    """Парсинг результата query запроса

    Args:
        data: результат GraphQL query запроса

        Пример:
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "closingIssuesReferences": {
                                "totalCount": 1,
                                "nodes": [
                                    {
                                        "id": "I_kwDOKUpUT86BE187",
                                        "title": "Some Issue Title",
                                        "number": 10,
                                        "projectItems": {
                                            "nodes": [
                                                {
                                                    "id": "PVTI_lAHOBUYqYc4AdPilzgNJ5Ag",
                                                    "fieldValueByName": {
                                                        "id": "PVTFSV_lQHOBUYqYc4AdPilzgNJ5AjOCVg--A",
                                                        "name": "Todo",
                                                        "optionId": "f75ad846"
                                                    },
                                                    "project": {
                                                        "id": "PVT_kwHOBUYqYc4AdPil",
                                                        "field": {
                                                            "id": "PVTSSF_lAHOBUYqYc4AdPilzgS85cY",
                                                            "name": "Status",
                                                            "options": [
                                                                {
                                                                    "id": "f75ad846",
                                                                    "name": "Todo"
                                                                },
                                                                {
                                                                    "id": "47fc9ee4",
                                                                    "name": "In Progress"
                                                                },
                                                                {
                                                                    "id": "a5657cb5",
                                                                    "name": "Approved"
                                                                },
                                                                {
                                                                    "id": "98236657",
                                                                    "name": "Done"
                                                                }
                                                            ]
                                                        }
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            }

    Returns:
        Данные для заполнения шаблона mutation-запроса
    """
    issues = data["data"]["repository"]["pullRequest"]["closingIssuesReferences"]["nodes"]
    for issue in issues:
        # XXX issue_hash_id = issue["id"]
        # XXX issue_number = issue["number"]
        project_items = issue["projectItems"]["nodes"]
        for project_item in project_items:
            item_hash_id = project_item["id"]
            field_value = project_item["fieldValueByName"]["name"]
            field_hash_id = project_item["project"]["field"]["id"]
            project_hash_id = project_item["project"]["id"]
            project_status_field = project_item["project"]["field"]
            field_options = {option["name"]: option["id"] for option in project_status_field["options"]}
            yield {
                "item_hash_id": item_hash_id,
                "field_hash_id": field_hash_id,
                "project_hash_id": project_hash_id,
                "field_options": field_options,
                "field_current_value": field_value,
            }


def define_new_status(pr_action: Action,
                      pr_state: State,
                      current_status: str | None,
                      field_options: dict[str, str],
                      ) -> dict[str, str]:
    """Логика определения нового статуса для задачи

    Args:
        pr_action: событие, по которому запустился GitHub Action
        pr_state: состояние review у Pull Request (если "" - pull_request_review события не было)
        current_status: наименование текущего статуса задачи
        field_options: словарь-маппинг наименования статуса задачи и его хэш id в GraphQL

    Returns:
        GraphQL hash id значения нового статуса задачи
    """
    if pr_action in ("converted_to_draft", "opened", "reopened"):
        status = "In Progress"
    elif pr_action == "ready_for_review":
        status = "Review"
    elif pr_state == "approved":
        status = "Approved"
    elif pr_state == "dismissed":
        status = "Review"
    else:
        status = current_status or "Todo"
    return {"field_value_hash_id": field_options[status], "field_value": status}


async def main() -> None:
    """Запуск логики обновления статуса проекта"""
    auth_token: str = os.environ["INPUT_PROJECT_TOKEN"]
    pr_action: Action = os.environ["INPUT_PR_ACTION"]  # type: ignore[assignment]
    pr_state: State = os.environ["INPUT_PR_STATE"]  # type: ignore[assignment]

    graphql_url: str = os.environ["GITHUB_GRAPHQL_URL"]

    data = {
        "repo_name": os.environ["GITHUB_REPOSITORY"].split("/")[-1],
        "repo_owner": os.environ["GITHUB_REPOSITORY_OWNER"],
        "pull_request_id": os.environ["GITHUB_REF_NAME"].split("/")[0],
    }

    _client_session_generator = create_client_session(auth_token)
    client_session = await anext(_client_session_generator)

    query = generate_query(QUERY_ISSUE_BY_PR, data)
    resp_json = await graphql_request(client_session, graphql_url, query)

    for result in parse_query_results(resp_json):
        new_status_value_info = define_new_status(
            pr_action, pr_state, result["field_current_value"], result["field_options"],
        )

        if result["field_current_value"] != new_status_value_info["field_value"]:
            data = {
                "item_hash_id": result["item_hash_id"],
                "field_hash_id": result["field_hash_id"],
                "project_hash_id": result["project_hash_id"],
                "field_value_hash_id": new_status_value_info["field_value_hash_id"],
            }
            mutation = generate_mutation(MUTATION_UPDATE_PROJECT_ITEM, data)
            await graphql_request(client_session, graphql_url, mutation)


if __name__ == "__main__":
    # local debugging
    # XXX from dotenv import load_dotenv
    # XXX load_dotenv()

    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())
