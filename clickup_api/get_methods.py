import datetime
import os
from typing import Annotated

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Query

from .exceptions import DateValueError, DateSequenceError, DateTypeError
from .handlers import (check_and_adjust_list_length,
                       date_as_string_to_unix_time_in_milliseconds,
                       split_string_array, split_int_array)

load_dotenv()

# uvicorn clickup_api.get_methods:app --reload

app = FastAPI()

# TOKEN = os.environ.get("CLICKUP_MY_TOKEN")
TOKEN = os.environ.get("CLICKUP_ADDITIONAL_TOKEN")
URL = os.environ.get("CLICKUP_URL")
HEADER = {"Authorization": TOKEN, "Content-Type": "application/json"}


@app.get("/authorized_teams_workspaces")
async def get_authorized_teams_workspaces():
    url = f"{URL}/team/"
    response = requests.get(url=url, headers=HEADER)
    return response.json()


@app.get("/teams")
async def get_teams(team_id: int | None = None, group_ids: str | None = None):
    url = f"{URL}/group"
    query = {"team_id": team_id, "group_ids": group_ids}
    response = requests.get(url, headers=HEADER, params=query)
    return response.json()


@app.get("/spaces/{team_id}")
async def get_spaces(team_id: int):
    url = f"{URL}/team/{str(team_id)}/space"
    response = requests.get(url, headers=HEADER)
    return response.json()


@app.get("/folders/{space_id}")
async def get_folders(space_id: int, archived: bool = False):
    url = f"{URL}/space/{str(space_id)}/folder"
    query = {"archived": "true" if archived else "false"}
    response = requests.get(url, headers=HEADER, params=query)
    return response.json()


@app.get("/lists/{folder_id}")
async def get_lists(folder_id: int, archived: bool = False):
    url = f"{URL}/folder/{str(folder_id)}/list"
    query = {"archived": "true" if archived else "false"}
    response = requests.get(url, headers=HEADER, params=query)
    return response.json()


@app.get("/tasks/{list_id}")
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
            description="Date in sequence: Year, Month, Day. \
            Use integers for date parameters. Use comma to separate parameters. \
                Example: 2024, 5, 15"
        ),
    ] = None,
    due_date_lt: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. \
            Use integers for date parameters. Use comma to separate parameters. \
                Example: 2024, 5, 15"
        ),
    ] = None,
    date_created_gt: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. \
            Use integers for date parameters. Use comma to separate parameters. \
                Example: 2024, 5, 15"
        ),
    ] = None,
    date_created_lt: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. \
            Use integers for date parameters. Use comma to separate parameters. \
                Example: 2024, 5, 15"
        ),
    ] = None,
    date_updated_gt: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. \
            Use integers for date parameters. Use comma to separate parameters. \
                Example: 2024, 5, 15"
        ),
    ] = None,
    date_updated_lt: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. \
            Use integers for date parameters. Use comma to separate parameters. \
                Example: 2024, 5, 15"
        ),
    ] = None,
    date_done_gt: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. \
            Use integers for date parameters. Use comma to separate parameters. \
                Example: 2024, 5, 15"
        ),
    ] = None,
    date_done_lt: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. \
            Use integers for date parameters. Use comma to separate parameters. \
                Example: 2024, 5, 15"
        ),
    ] = None,
    # custom_fields: list[str] | None = None,  # NotImplemented
    custom_items: Annotated[
        list[str] | None,
        Query(description="Filter by custom task types. Use comma to separate items.\
            Including 0 returns tasks. Including 1 returns Milestones. Including any \
                other number returns the custom task type as defined in your Workspace."),
    ] = None,
):
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


@app.get("/task/{task_id}")
async def get_task(
    task_id: str,
    custom_task_ids: bool = False,
    team_id: int | None = None,
    include_subtasks: bool = False,
    include_markdown_description: bool = False,
):
    url = f"{URL}/task/{str(task_id)}"

    custom_task_ids = "true" if team_id or custom_task_ids else "false"

    query = {
        "custom_task_ids": custom_task_ids,
        "team_id": team_id,
        "include_subtasks": "true" if include_subtasks else "false",
        "include_markdown_description": "true" if include_markdown_description else "false",
    }

    response = requests.get(url, headers=HEADER, params=query)
    return response.json()


@app.get("/user/{team_id}/{user_id}")
async def get_user(team_id: int, user_id: int):
    url = f"{URL}/team/{str(team_id)}/user/{str(user_id)}"
    response = requests.get(url, headers=HEADER)
    return response.json()


@app.get("/team/{team_id}/time_entries")
async def get_time_entries(
    team_id: int,
    start_date: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. \
            Use integers for date parameters. Use comma to separate parameters. \
                Example: 2024, 5, 15"
        ),
    ] = None,
    end_date: Annotated[
        str | None,
        Query(
            description="Date in sequence: Year, Month, Day. \
            Use integers for date parameters. Use comma to separate parameters. \
                Example: 2024, 5, 15"
        ),
    ] = None,
    assignee: Annotated[
        int | str | None,
        Query(description="Filter by user_id. For multiple assignees, separate user_id using commas.")
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
        Query(description="Only used when the custom_task_ids parameter is set to true.")
        ] = None,
):
    url = f"{URL}/team/{str(team_id)}/time_entries"

    custom_task_ids = "true" if query_team_id or custom_task_ids else "false"

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
