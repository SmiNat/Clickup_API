import datetime
import os
from typing import Annotated

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Query

from .exceptions import DateDataError, DateSequenceError, DateTypeError
from .handlers import (check_and_adjust_list_length,
                       date_as_string_to_unix_time_in_milliseconds,
                       split_array)

load_dotenv()

# uvicorn clickup_api.get_methods:app --reload

app = FastAPI()

TOKEN = os.environ.get("CLICKUP_MY_TOKEN")
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
    # custom_items: list[int] | None = None,
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
        "statuses": split_array(statuses),
        "include_closed": "true" if include_closed else "false",
        "assignees": split_array(assignees),
        "tags": split_array(tags),
        "due_date_gt": date_as_string_to_unix_time_in_milliseconds(due_date_gt),
        "due_date_lt": date_as_string_to_unix_time_in_milliseconds(due_date_lt),
        "date_created_gt": date_as_string_to_unix_time_in_milliseconds(date_created_gt),
        "date_created_lt": date_as_string_to_unix_time_in_milliseconds(date_created_lt),
        "date_updated_gt": date_as_string_to_unix_time_in_milliseconds(date_updated_gt),
        "date_updated_lt": date_as_string_to_unix_time_in_milliseconds(date_updated_lt),
        "date_done_gt": date_as_string_to_unix_time_in_milliseconds(date_done_gt),
        "date_done_lt": date_as_string_to_unix_time_in_milliseconds(date_done_lt),
        # "custom_fields": custom_fields,
        # "custom_items": custom_items,
    }

    response = requests.get(url, headers=HEADER, params=query)
    return response.json()
