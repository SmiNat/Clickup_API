import requests
from fastapi import APIRouter, HTTPException, Query, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from starlette import status
from typing import Annotated, Optional, Type

from ..enums import Static
from ..utils import header, validate_token
from clickup_api.handlers import (
    date_as_dict_to_unix_time_in_milliseconds,
    time_as_dict_to_unix_time_in_milliseconds
    )
from .get_methods import get_task

router = APIRouter(tags=["ClickUp post/put methods"])

URL = Static.URL.value


class DateRequest(BaseModel):
    year: int = Field(default=None, gt=2000, examples=[2024])
    month: int = Field(default=None, gt=0, lt=13, examples=[3])
    day: int = Field(default=None, gt=0, lt=32, examples=[25])


class TimeEstimate(BaseModel):
    days: int = Field(default=None, ge=0, examples=[0])
    hours: int = Field(default=None, ge=0, examples=[4])
    minutes: int = Field(default=None, ge=0, examples=[30])


class CustomFields(BaseModel):
    id: str = Field(description="Field id",
                    examples=["abcd1234-xzy1-987a-11bb-abd1234xyz987"])
    value: str | int = Field(examples=["String to added to a Custom Field"])


class EditAssignees(BaseModel):
    add: list[int] | None = None
    rem: list[int] | None = None


class TaskBasicRequest(BaseModel):
    name: str = Field(min_length=1, examples=["New task name"])
    description: str | None = Field(default=None, examples=["Task description"])
    parent: str | None = Field(default=None,
                               title="Parent task id",
                               description="You can create a subtask by including "
                               "an existing task ID. The parent task ID you include "
                               "cannot be a subtask, and must be in the same List "
                               "specified in the path parameter.",
                               examples=[None])
    status: str | None = Field(default=None, examples=["nowe"])
    priority: int | None = Field(default=4)
    due_date: DateRequest | None = None
    due_date_time: bool = False
    time_estimate: TimeEstimate | None = None
    start_date: Optional[DateRequest] = None
    start_date_time: bool = False


class CreateTaskFullRequest(TaskBasicRequest):
    assignees: list[int | None] | None = Field(default=None,
                                               title="Assignees ids",
                                               examples=[[None]])
    tags: list[str] | None = Field(default=None, examples=[["bugs", "backend"]])
    notify_all: bool = False
    links_to: str | None = Field(default=None, examples=[None])
    check_required_custom_fields: bool = False
    custom_fields: list[CustomFields] | None = Field(default=None,
                                                     description="More information: "
                                                     "https://clickup.com/api/developer-portal/filtertasks/")
    custom_item_id: int | None = Field(default=None,
                                       description="To create a task that doesn't use "
                                       "a custom task type, either don't include this "
                                       "field in the request body, or send 'null'. "
                                       "To create this task as a Milestone, send "
                                       "a value of 1.To use a custom task type, send "
                                       "the custom task type ID as defined in your "
                                       "Workspace, such as 2.")


class UpdateTaskFullRequest(TaskBasicRequest):
    assignees: EditAssignees | None = None
    archived: bool = False


class CreateChecklist(BaseModel):
    name: str = Field(min_length=1)


class UpdateChecklist(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    position: int | None = Field(default=None, description="Position refers to the "
                                 "order of appearance of checklists on a task. To set "
                                 "a checklist to appear at the top of the checklists "
                                 "section of a task, use 'position': 0.")


class CreateChecklistItem(BaseModel):
    name: str = Field(min_length=1)
    assignee: int | None = Field(default=None, examples=[None])


class UpdateChecklistItem(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    assignee: int | None = Field(default=None, examples=[None])
    remove_assignee: bool = Field(default=False, description="To remove Assignee from "
                                  "an item and leave it empty. Always False if assignee "
                                  "is not None")
    resolved: bool = False
    parent: str | None = Field(default=None, description="To nest a checklist item "
                               "under another checklist item, include the other item's "
                               "checklist_item_id.", examples=[None])


@router.post("/list/{list_id}/task", status_code=status.HTTP_201_CREATED)
async def create_task(
    list_id: int,
    task: CreateTaskFullRequest,
    custom_task_ids: bool = False,
    team_id: int | None = None,
    token: str | None = None
):
    validate_token(token)
    url = f"{URL}/list/{str(list_id)}/task"

    custom_task_ids = "true" if team_id or custom_task_ids else "false"

    query = {"custom_task_ids": custom_task_ids, "team_id": team_id}

    # print("✅ task: ", task)
    update_task_encoded = jsonable_encoder(task)
    # print("✅ task json: ", update_task_encoded)

    if update_task_encoded["due_date"]:
        update_task_encoded["due_date"] = date_as_dict_to_unix_time_in_milliseconds(
            update_task_encoded["due_date"])
    if update_task_encoded["start_date"]:
        update_task_encoded["start_date"] = date_as_dict_to_unix_time_in_milliseconds(
            update_task_encoded["start_date"])
    if update_task_encoded["time_estimate"]:
        update_task_encoded["time_estimate"] = time_as_dict_to_unix_time_in_milliseconds(
            update_task_encoded["time_estimate"])

    # print("✅ task json update: ", update_task_encoded)

    response = requests.post(url, headers=header(token), params=query,
                             json=update_task_encoded)
    # print("✅ task json: ", response.json())
    if not response.status_code < 400:
        raise HTTPException(response.status_code, response.json())
    return response.json()


@router.put("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def edit_task(
    task_id: str,
    task: UpdateTaskFullRequest,
    custom_task_ids: bool = False,
    team_id: int | None = None,
    token: str | None = None
):
    validate_token(token)
    url = f"{URL}/task/{str(task_id)}"

    custom_task_ids = "true" if team_id or custom_task_ids else "false"

    query = {"custom_task_ids": custom_task_ids, "team_id": team_id}

    update_task_encoded = jsonable_encoder(task)

    if update_task_encoded["due_date"]:
        update_task_encoded["due_date"] = date_as_dict_to_unix_time_in_milliseconds(
            update_task_encoded["due_date"])
    if update_task_encoded["start_date"]:
        update_task_encoded["start_date"] = date_as_dict_to_unix_time_in_milliseconds(
            update_task_encoded["start_date"])
    if update_task_encoded["time_estimate"]:
        update_task_encoded["time_estimate"] = time_as_dict_to_unix_time_in_milliseconds(
            update_task_encoded["time_estimate"])

    response = requests.put(url, headers=header(token), params=query, json=update_task_encoded)
    if not response.status_code < 400:
        raise HTTPException(response.status_code, response.json())
    return response.json()


@router.post("/task/{task_id}/checklist", status_code=status.HTTP_201_CREATED)
async def create_checklist(
    task_id: str,
    name: CreateChecklist,
    custom_task_ids: bool = False,
    team_id: int | None = None,
    token: str | None = None
):
    validate_token(token)
    url = f"{URL}/task/{str(task_id)}/checklist"

    custom_task_ids = "true" if team_id or custom_task_ids else "false"

    query = {"custom_task_ids": custom_task_ids,  "team_id": team_id}

    response = requests.post(url, headers=header(token), params=query,
                             json=jsonable_encoder(name))
    if not response.status_code < 400:
        raise HTTPException(response.status_code, response.json())
    return response.json()


@router.put("/checklist/{checklist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def edit_checklist(
    checklist_id: str,
    name: UpdateChecklist,
    token: str | None = None
):
    validate_token(token)
    url = f"{URL}/checklist/{str(checklist_id)}"

    response = requests.put(url, headers=header(token), json=jsonable_encoder(name))
    if not response.status_code < 400:
        raise HTTPException(response.status_code, response.json())
    return response.json()


@router.post("/checklist/{checklist_id}/checklist_item",
             status_code=status.HTTP_201_CREATED)
async def create_checklist_item(
    checklist_id: str,
    item: CreateChecklistItem,
    token: str | None = None
):
    validate_token(token)
    url = f"{URL}/checklist/{str(checklist_id)}/checklist_item"

    response = requests.post(url, headers=header(token), json=jsonable_encoder(item))
    if not response.status_code < 400:
        raise HTTPException(response.status_code, response.json())
    return response.json()


@router.put("/checklist/{checklist_id}/checklist_item/{checklist_item_id}",
            status_code=status.HTTP_204_NO_CONTENT)
async def edit_checklist_item(
    checklist_id: str,
    checklist_item_id: str,
    task_id: str,
    item: UpdateChecklistItem,
    token: str | None = None
):
    validate_token(token)
    url = f"{URL}/checklist/{str(checklist_id)}/checklist_item/{str(checklist_item_id)}"

    item_encoded = jsonable_encoder(item)
    # print("✅ item:", item_encoded)

    if not item_encoded["name"] or not item_encoded["assignee"]:
        task = await get_task(task_id)
        # print("✅ task:", task)
        for checklist in task["checklists"]:
            if checklist["id"] == checklist_id:
                task_checklist = checklist
                break
        for item in task_checklist["items"]:
            if item["id"] == checklist_item_id:
                # print("✅ item:", item)
                name = item["name"]
                assignee = None if not item["assignee"] else item["assignee"]["id"]
                break

    if not item_encoded["name"]:
        item_encoded["name"] = name
    if not item_encoded["assignee"]:
        item_encoded["assignee"] = None if item_encoded["remove_assignee"] else assignee

    # print("✅ item updated", item_encoded)

    response = requests.put(url, headers=header(token), json=item_encoded)
    if not response.status_code < 400:
        raise HTTPException(response.status_code, response.json())
    return response.json()
