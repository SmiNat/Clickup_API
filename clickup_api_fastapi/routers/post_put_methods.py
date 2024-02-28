import requests
from fastapi import APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from starlette import status
from typing import Annotated, Optional

from ..enums import Static
from clickup_api.handlers import (
    date_as_dict_to_unix_time_in_milliseconds,
    time_as_dict_to_unix_time_in_milliseconds
    )

router = APIRouter(tags=["post/put methods"])

HEADER = {"Authorization": Static.TOKEN.value, "Content-Type": "application/json"}
URL = Static.URL.value



class DateRequest(BaseModel):
    year: int = Field(default=2024, gt=2000)
    month: int = Field(default=3, gt=0, lt=13)
    day: int = Field(default=22, gt=0, lt=32)


class TimeEstimate(BaseModel):
    days: int = Field(default=0, ge=0)
    hours: int = Field(default=4, ge=0)
    minutes: int = Field(default=0, ge=0)


class CustomFields(BaseModel):
    id: str
    value: str | int


class CreateTaskRequest(BaseModel):
    name: str = Field(min_length=1, title="Task name")
    description: str | None =  None
    parent: str | None = Field(default=None,
                               title="Parent task id",
                               description="You can create a subtask by including "
                               "an existing task ID. The parent task ID you include "
                               "cannot be a subtask, and must be in the same List "
                               "specified in the path parameter.")
    assignees: list[int] | None = Field(default=None, title="Assignees ids")
    tags: list[str] | None = None
    status: str | None = None
    priority: int | None = None
    due_date: DateRequest | None = None
    due_date_time: bool = False
    time_estimate: TimeEstimate | None = None
    start_date: Optional[DateRequest] = None
    start_date_time: bool = False
    notify_all: bool = False
    links_to: str | None = None
    check_required_custom_fields: bool = False
    custom_fields: list[CustomFields] | None = None
    custom_item_id: int | None = None


@router.post("/list/{list_id}/task", status_code=status.HTTP_201_CREATED)
# @router.post("/test")
async def create_task(
    list_id: int,
    task: CreateTaskRequest,
    custom_task_ids: bool = False,
    team_id: int | None = None,
):
    url = f"{URL}/list/{str(list_id)}/task"
    # url = f"http://127.0.0.1:8000/test"

    custom_task_ids = "true" if team_id or custom_task_ids else "false"

    query = {
        "custom_task_ids": custom_task_ids,
        "team_id": team_id,
    }

    update_task_encoded = jsonable_encoder(task)

    if update_task_encoded["due_date"]:
        update_task_encoded["due_date"] = date_as_dict_to_unix_time_in_milliseconds(update_task_encoded["due_date"])
    if update_task_encoded["start_date"]:
        update_task_encoded["start_date"] = date_as_dict_to_unix_time_in_milliseconds(update_task_encoded["start_date"])
    if update_task_encoded["time_estimate"]:
        update_task_encoded["time_estimate"] = time_as_dict_to_unix_time_in_milliseconds(update_task_encoded["time_estimate"])

    print(update_task_encoded)
    print(type(update_task_encoded))

    response = requests.post(url, headers=HEADER, params=query, json=update_task_encoded)
    print(response.json())
    return response.json()
    # return task


