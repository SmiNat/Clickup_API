import datetime
from typing import Annotated

import requests
from fastapi import APIRouter, Query

from clickup_api.handlers import (
    date_as_string_to_unix_time_in_milliseconds,
    split_int_array,
    split_string_array,
)
from clickup_api_fastapi.enums import Static

# uvicorn clickup_api_fastapi.main:app --reload

router = APIRouter(tags=["get methods"])

HEADER = {"Authorization": Static.TOKEN.value, "Content-Type": "application/json"}
URL = Static.URL.value


@router.get("/authorized_user")
async def get_authorized_user():
    url = f"{URL}/user"
    response = requests.get(url, headers=HEADER)
    return response.json()


@router.get("/authorized_teams_workspaces")
async def get_authorized_teams_workspaces():
    url = f"{URL}/team/"
    response = requests.get(url=url, headers=HEADER)
    return response.json()


@router.get("/group")
async def get_teams(
    team_id: Annotated[
        int | None, Query(description="Refers to the id of a Workspace.")
    ] = None,
    group_ids: Annotated[
        str | None, Query(description="Refers to the id of a user group.")
    ] = None,
):
    """This endpoint is used to view Teams: user groups in your Workspace."""

    url = f"{URL}/group"
    query = {"team_id": team_id, "group_ids": group_ids}
    response = requests.get(url, headers=HEADER, params=query)
    return response.json()


@router.get("/team/{team_id}/space")
async def get_spaces(team_id: int):
    url = f"{URL}/team/{str(team_id)}/space"
    response = requests.get(url, headers=HEADER)
    return response.json()


@router.get("/space/{space_id}")
async def get_space(space_id: int):
    url = f"{URL}/space/{str(space_id)}"
    response = requests.get(url, headers=HEADER)
    return response.json()


@router.get("/space/{space_id}/folder")
async def get_folders(space_id: int, archived: bool = False):
    url = f"{URL}/space/{str(space_id)}/folder"
    query = {"archived": "true" if archived else "false"}
    response = requests.get(url, headers=HEADER, params=query)
    return response.json()


@router.get("/folder/{folder_id}")
async def get_folder(folder_id: int):
    url = f"{URL}/folder/{str(folder_id)}"
    response = requests.get(url, headers=HEADER)
    return response.json()


@router.get("/folder/{folder_id}/list")
async def get_lists(folder_id: int, archived: bool = False):
    url = f"{URL}/folder/{str(folder_id)}/list"
    query = {"archived": "true" if archived else "false"}
    response = requests.get(url, headers=HEADER, params=query)
    return response.json()


@router.get("/list/{list_id}")
async def get_list(list_id: int):
    url = f"{URL}/list/{str(list_id)}"
    response = requests.get(url, headers=HEADER)
    return response.json()


@router.get("/space/{space_id}/list")
async def get_folderless_lists(space_id: int, archived: bool = False):
    url = f"{URL}/space/{str(space_id)}/list"
    query = {"archived": "true" if archived else "false"}
    response = requests.get(url, headers=HEADER, params=query)
    return response.json()


@router.get("/list/{list_id}/task")
async def get_tasks(
    list_id: int,
    archived: bool = False,
    include_markdown_description: bool = False,
    page: int = 0,
    order_by: Annotated[
        str,
        Query(description="Available options: 'created', 'updated', 'id', 'due_date'."),
    ] = "created",
    reverse: bool = False,
    subtasks: bool = False,
    statuses: Annotated[
        list[str] | None,
        Query(description="Filter by statuses. Use comma to separate statuses."),
    ] = None,
    include_closed: bool = False,
    assignees: Annotated[
        list[int | str] | None,
        Query(description="Filter by Assignees. Use comma to separate ids."),
    ] = None,
    tags: Annotated[
        list[str] | None,
        Query(description="Filter by tags. Use comma to separate tags."),
    ] = None,
    due_date_gt: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. "
            "Use integers for date parameters. Use comma to separate parameters. "
            "Example: 2024, 5, 15."
        ),
    ] = None,
    due_date_lt: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. "
            "Use integers for date parameters. Use comma to separate parameters. "
            "Example: 2024, 5, 15."
        ),
    ] = None,
    date_created_gt: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. "
            "Use integers for date parameters. Use comma to separate parameters. "
            "Example: 2024, 5, 15."
        ),
    ] = None,
    date_created_lt: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. "
            "Use integers for date parameters. Use comma to separate parameters. "
            "Example: 2024, 5, 15."
        ),
    ] = None,
    date_updated_gt: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. "
            "Use integers for date parameters. Use comma to separate parameters. "
            "Example: 2024, 5, 15."
        ),
    ] = None,
    date_updated_lt: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. "
            "Use integers for date parameters. Use comma to separate parameters. "
            "Example: 2024, 5, 15."
        ),
    ] = None,
    date_done_gt: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. "
            "Use integers for date parameters. Use comma to separate parameters. "
            "Example: 2024, 5, 15."
        ),
    ] = None,
    date_done_lt: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. "
            "Use integers for date parameters. Use comma to separate parameters. "
            "Example: 2024, 5, 15."
        ),
    ] = None,
    # custom_fields: list[str] | None = None,  # NotImplemented
    custom_items: Annotated[
        list[str] | None,
        Query(
            description="Filter by custom task types. Use comma to separate items. "
            "Including 0 returns tasks. Including 1 returns Milestones. Including any "
            "other number returns the custom task type as defined in your Workspace."
        ),
    ] = None,
):
    """Responses are limited to 100 tasks per page.
    You can only view task information of tasks you can access.
    This endpoint only includes tasks where the specified list_id is their home List.
    Tasks added to the list_id with a different home List are not included in the response.
    """

    url = f"{URL}/list/{str(list_id)}/task"

    query = {
        "archived": "true" if archived else "false",
        "include_markdown_description": (
            "true" if include_markdown_description else "false"
        ),
        "page": page,
        "order_by": order_by,
        "reverse": "true" if reverse else "false",
        "subtasks": "true" if subtasks else None,
        "statuses": split_string_array(statuses),
        "include_closed": "true" if include_closed else "false",
        "assignees": split_string_array(assignees),
        "tags": split_string_array(tags),
        "due_date_gt": date_as_string_to_unix_time_in_milliseconds(due_date_gt),
        "due_date_lt": date_as_string_to_unix_time_in_milliseconds(due_date_lt),
        "date_created_gt": date_as_string_to_unix_time_in_milliseconds(date_created_gt),
        "date_created_lt": date_as_string_to_unix_time_in_milliseconds(date_created_lt),
        "date_updated_gt": date_as_string_to_unix_time_in_milliseconds(date_updated_gt),
        "date_updated_lt": date_as_string_to_unix_time_in_milliseconds(date_updated_lt),
        "date_done_gt": date_as_string_to_unix_time_in_milliseconds(date_done_gt),
        "date_done_lt": date_as_string_to_unix_time_in_milliseconds(date_done_lt),
        # "custom_fields": custom_fields,
        "custom_items": split_int_array(custom_items),
    }

    response = requests.get(url, headers=HEADER, params=query)
    return response.json()


@router.get("/task/{task_id}")
async def get_task(
    task_id: str,
    custom_task_ids: bool = False,
    team_id: int | None = None,
    include_subtasks: bool = False,
    include_markdown_description: bool = False,
):
    """You can only view task information of tasks you can access."""

    url = f"{URL}/task/{str(task_id)}"

    custom_task_ids = "true" if team_id or custom_task_ids else "false"

    query = {
        "custom_task_ids": custom_task_ids,
        "team_id": team_id,
        "include_subtasks": "true" if include_subtasks else "false",
        "include_markdown_description": (
            "true" if include_markdown_description else "false"
        ),
    }

    response = requests.get(url, headers=HEADER, params=query)
    return response.json()


@router.get("/team/{team_id}/user/{user_id}")
async def get_user(team_id: int, user_id: int):
    """This endpoint is only available to Workspaces on Enterprise Plan."""

    url = f"{URL}/team/{str(team_id)}/user/{str(user_id)}"
    response = requests.get(url, headers=HEADER)
    return response.json()


@router.get("/team/{team_id}/time_entries")
async def get_time_entries(
    team_id: int,
    start_date: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. "
            "Use integers for date parameters. Use comma to separate parameters. "
            "Example: 2024, 5, 15. If None, equals to the beginning of the current month."
        ),
    ] = None,
    end_date: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. "
            "Use integers for date parameters. Use comma to separate parameters. "
            "Example: 2024, 5, 15"
        ),
    ] = None,
    assignee: Annotated[
        int | str | None,
        Query(
            description="Filter by user_id. For multiple assignees, separate user_id "
            "using commas."
        ),
    ] = None,
    include_task_tags: bool = False,
    include_location_names: bool = False,
    space_id: int | None = None,
    folder_id: int | None = None,
    list_id: int | None = None,
    task_id: str | None = None,
    custom_task_ids: bool = False,
    query_team_id: Annotated[
        int | None,
        Query(
            description="Only used when the custom_task_ids parameter is set to true."
        ),
    ] = None,
):
    url = f"{URL}/team/{str(team_id)}/time_entries"

    custom_task_ids = "true" if query_team_id or custom_task_ids else "false"
    if not start_date:
        start_date = (
            str(datetime.date.today().year)
            + ","
            + str(datetime.date.today().month)
            + ",1"
        )

    query = {
        "start_date": date_as_string_to_unix_time_in_milliseconds(start_date),
        "end_date": date_as_string_to_unix_time_in_milliseconds(end_date),
        "assignee": assignee,
        "include_task_tags": "true" if include_task_tags else "false",
        "include_location_names": "true" if include_location_names else "false",
        "space_id": space_id,
        "folder_id": folder_id,
        "list_id": list_id,
        "task_id": task_id,
        "custom_task_ids": custom_task_ids,
        "team_id": query_team_id,
    }

    response = requests.get(url, headers=HEADER, params=query)
    return response.json()


@router.get("/task/{task_id}/comment")
async def get_task_comments(
    task_id: str,
    custom_task_ids: bool = False,
    team_id: int | None = None,
    start: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. "
            "Use integers for date parameters. Use comma to separate parameters. "
            "Example: 2024, 5, 15."
        ),
    ] = None,
    start_id: Annotated[
        str | None, Query(description="Enter the Comment id of a task comment.")
    ] = None,
):
    """If you do not include the start and start_id parameters, this endpoint will
    return the most recent 25 comments. Use the start and start id parameters of the
    oldest comment to retrieve the next 25 comments."""

    url = f"{URL}/task/{str(task_id)}/comment"

    custom_task_ids = "true" if team_id or custom_task_ids else "false"

    query = {
        "custom_task_ids": custom_task_ids,
        "team_id": team_id,
        "start": date_as_string_to_unix_time_in_milliseconds(start),
        "start_id": start_id,
    }

    response = requests.get(url, headers=HEADER, params=query)
    return response.json()


@router.get("/list/{list_id}/comment")
async def get_list_comments(
    list_id: int,
    start: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. "
            "Use integers for date parameters. Use comma to separate parameters. "
            "Example: 2024, 5, 15."
        ),
    ] = None,
    start_id: Annotated[
        str | None, Query(description="Enter the Comment id of a task comment")
    ] = None,
):
    """If you do not include the start and start_id parameters, this endpoint will
    return the most recent 25 comments. Use the start and start id parameters of the
    oldest comment to retrieve the next 25 comments."""

    url = f"{URL}/list/{int(list_id)}/comment"

    query = {
        "start": date_as_string_to_unix_time_in_milliseconds(start),
        "start_id": start_id,
    }

    response = requests.get(url, headers=HEADER, params=query)
    return response.json()


@router.get("/view/{view_id}/comment")
async def get_chat_view_comments(
    view_id: str,
    start: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. "
            "Use integers for date parameters. Use comma to separate parameters. "
            "Example: 2024, 5, 15."
        ),
    ] = None,
    start_id: Annotated[
        str | None, Query(description="Enter the Comment id of a task comment")
    ] = None,
):
    """If you do not include the start and start_id parameters, this endpoint will
    return the most recent 25 comments. Use the start and start id parameters of the
    oldest comment to retrieve the next 25 comments."""

    url = f"{URL}/view/{str(view_id)}/comment"

    query = {
        "start": date_as_string_to_unix_time_in_milliseconds(start),
        "start_id": start_id,
    }

    response = requests.get(url, headers=HEADER, params=query)
    return response.json()


@router.get("/team/{team_id}/custom_item")
async def get_custom_task_types(team_id: int):
    url = f"{URL}/team/{int(team_id)}/custom_item"
    response = requests.get(url, headers=HEADER)
    return response.json()


@router.get("/list/{list_id}/field")
async def get_accessible_custom_fields(list_id: int):
    url = f"{URL}/list/{int(list_id)}/field"
    response = requests.get(url, headers=HEADER)
    return response.json()
