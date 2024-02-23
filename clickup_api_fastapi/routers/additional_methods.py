import datetime
from typing import Annotated, Any

from fastapi import APIRouter, HTTPException, Query
from starlette import status

from clickup_api.handlers import split_int_array
from clickup_api_fastapi.routers.get_methods import (
    get_authorized_teams_workspaces, get_time_entries)

router = APIRouter(tags=["new methods"])


async def request_workspace_ids(team_id: Any | None = None) -> list | tuple:
    """
    If no 'team_id' - returns a list of workspaces (team_ids) authorized for a token
    owner from get_authorized_teams_workspaces request.
    If 'team_id' is provided, verifies if type of data for 'team_id' is correct.

    Args:
        team_id (Any | None, optional):
            Team ID (Workspace). If None, includes all teams available for token owner.
            Defaults to None.
        token (str | None, optional):
            Token for request authentication. If None, uses token of an instance.
            Defaults to None.
    Returns:
        list | tuple:
            Returns a list or a tuple of team_ids (workspaces).
    """

    if not team_id:
        workspaces = await get_authorized_teams_workspaces()
        if not workspaces["teams"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=("No teams (workspaces) found for a given token."),
            )
        teams = []
        for team in workspaces["teams"]:
            teams.append(team["id"])
    elif isinstance(team_id, (list, tuple)):
        teams = team_id
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"'team_id' must be a list or a tuple, not {type(team_id)}.",
        )
    return teams


async def request_time_entries_for_workspace_ids(
    team_id: list[int] | tuple[int], **kwargs
) -> list:
    """
    Returns a list of responses from get_time_entries request on each team (workspace).

    Args:
        team_id (list[int] | tuple[int]):
            Team ID (Workspace).
    Returns:
        list:
            Returns a list of responses to get_time_entries request.
    """

    if not team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="'team_id' must be a list or a tuple with ID values.",
        )

    responses = []
    for team in team_id:
        response = await get_time_entries(team_id=team, **kwargs)
        if not "data" in response.keys():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Team not authorized for a given token user. "
                "Change 'team_id' parameter or upgrade token value.",
            )
        else:
            responses.append(response)
    return responses


@router.get("/additional/user_worktime", status_code=status.HTTP_200_OK)
async def user_worktime(
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
        list[int | str] | None,
        Query(description="Filter by Assignees. Use comma to separate ids."),
    ] = None,
    team_id: Annotated[list[int] | None, Query()] = None,
    only_billable: bool = False,
):
    workspaces = await request_workspace_ids(team_id=team_id)

    time_entry_responses = await request_time_entries_for_workspace_ids(
        workspaces,
        start_date=start_date,
        end_date=end_date,
        assignee=assignee,
    )

    duration_per_user = {}
    for response in time_entry_responses:
        for task in response["data"]:
            if task["user"]["username"] in duration_per_user:
                if only_billable:
                    duration_per_user[task["user"]["username"]] += (
                        int(task["duration"]) if task["billable"] else 0
                    )
                else:
                    duration_per_user[task["user"]["username"]] += int(task["duration"])
            else:
                if only_billable:
                    duration_per_user[task["user"]["username"]] = (
                        int(task["duration"]) if task["billable"] else 0
                    )
                else:
                    duration_per_user[task["user"]["username"]] = int(task["duration"])

    for user, duration in duration_per_user.items():
        duration_per_user[user] = str(
            datetime.timedelta(seconds=int(duration) / 1000)
        ).split(".")[0]

    return duration_per_user


@router.get("/additional/user_tasks")
async def user_tasks(
    username: str,
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
    team_id: Annotated[
        list[int | str] | None,
        Query(
            description="Team ID (Workspace). Note: one user may be assigned to more \
                than one team. To receive tasks from multiple workspaces, use comma to \
                    separate team IDs. If None, includes all teams available for \
                        token owner. Defaults to None."
        ),
    ] = None,
):

    # cleaning team_id of trailing commas and spaces
    if team_id:
        team_id = [team_id[0].strip().strip(",")]
        # converting string with numbers into list of integers
        if "," in team_id[0]:
            try:
                team_id = split_int_array(team_id)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="'team_id' must contain numbers separated by commas.",
                )
    workspaces_ids = await request_workspace_ids(team_id=team_id)

    # for filtering by username and surname instead of user_id:
    workspaces_data = await get_authorized_teams_workspaces()
    for team in workspaces_data["teams"]:
        is_user_in_workspace = False
        for user in team["members"]:
            if username.casefold() == user["user"]["username"].casefold():
                assignee = user["user"][
                    "id"
                ]  # getting user_id from username from workspace
                is_user_in_workspace = True
                break

    if not is_user_in_workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{username}' not found in workspace list of members.  "
            "Validate 'username' argument or use another token to search "
            "through different workspaces.",
        )

    time_entry_responses = await request_time_entries_for_workspace_ids(
        workspaces_ids,
        start_date=start_date,
        end_date=end_date,
        assignee=assignee,
        custom_task_ids=True,
    )

    # all unique tasks by ids (one task can appear many times depending on the number of times tracked):
    task_ids = []
    # all time tracked ids for all tasks (each time track has its own id):
    task_entry_ids = []

    user_tasks = {
        "username": username,
        "user_id": assignee,
        "tasks": [],
    }

    # if there is more than one workspace to get tasks from, the access to response data
    # for each workspace must be made separately:
    for response in time_entry_responses:
        # accessing response data from request made on get_time_entries on each workspace:
        if response["data"]:
            for task in response["data"]:
                # increasing time duration for existing task in user_tasks dict (task with multiple time entrances):
                if task["task"]["id"] in task_ids:
                    for element in user_tasks["tasks"]:
                        if task["task"]["id"] == element["task_id"]:
                            element["duration"] += int(task["duration"])
                            task_entry_ids.append(task["id"])
                # adding a new task to user_tasks dict:
                else:
                    task_entry_ids.append(task["id"])
                    task_ids.append(task["task"]["id"])
                    new_task = {}
                    new_task["task_id"] = (
                        task["task"]["id"] if "task" in task.keys() else None
                    )
                    new_task["custom_id"] = (
                        task["task"]["custom_id"]
                        if "task" in task.keys() and "custom_id" in task["task"].keys()
                        else None
                    )
                    new_task["task_name"] = (
                        task["task"]["name"] if "task" in task.keys() else None
                    )
                    new_task["duration"] = (
                        int(task["duration"]) if "duration" in task.keys() else None
                    )
                    new_task["custom_id"] = (
                        task["custom_items"]["id"]
                        if "custom_items" in task.keys()
                        else None
                    )
                    user_tasks["tasks"].append(new_task)

    # converting Epoch time to datetime for each task:
    for task in user_tasks["tasks"]:
        task["duration"] = str(
            datetime.timedelta(seconds=int(task["duration"]) / 1000)
        ).split(".")[0]

    # DEBUG:
    # print("✅ data set:", time_entry_responses)
    # print("✅ task_ids:", task_ids, "list length:", len(task_ids))
    # print("✅ task_entry_ids:", task_entry_ids, "list length:", len(task_entry_ids))

    return user_tasks
