import requests
from fastapi import APIRouter, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..enums import Static
from ..utils import header, validate_token

router = APIRouter(tags=["ClickUp delete methods"])

URL = Static.URL


@router.delete("/comment/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: str, token: str | None = None):
    validate_token(token)
    url = f"{URL}/comment/{str(comment_id)}"
    response = requests.delete(url, headers=header(token=token))
    if not response.status_code < 400:
        raise HTTPException(response.status_code, response.json())
    return response.json()


@router.delete("/list/{list_id}/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_task_from_a_list(list_id: int, task_id: str, token: str | None = None):
    """
    Remove a task from an additional List. You can't remove a task from its home List.
    Note: This endpoint requires the Tasks in Multiple List ClickApp to be enabled.
    """
    validate_token(token)
    url = f"{URL}/list/{str(list_id)}/task/{str(task_id)}"
    response = requests.delete(url, headers=header(token=token))
    if not response.status_code < 400:
        raise HTTPException(response.status_code, response.json())
    return response.json()


@router.delete("/task/{task_id}")
async def delete_task(task_id: str, token: str | None = None):
    validate_token(token)
    url = f"{URL}/task/{str(task_id)}"
    response = requests.delete(
        url, headers=header(token=token, content_type="application/json")
    )
    if not response.status_code < 400:
        raise HTTPException(response.status_code, response.json())
    return JSONResponse(content=jsonable_encoder(response))


@router.delete("/checklist/{checklist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_checklist(checklist_id: str, token: str | None = None):
    validate_token(token)
    url = f"{URL}/checklist/{str(checklist_id)}"
    response = requests.delete(url, headers=header(token=token))
    if not response.status_code < 400:
        raise HTTPException(response.status_code, response.json())
    return response.json()


@router.delete(
    "/checklist/{checklist_id}/checklist_item/{checklist_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_checklist_item(
    checklist_id: str, checklist_item_id: str, token: str | None = None
):
    validate_token(token)
    url = f"{URL}/checklist/{str(checklist_id)}/checklist_item/{str(checklist_item_id)}"
    response = requests.delete(url, headers=header(token=token))
    if not response.status_code < 400:
        raise HTTPException(response.status_code, response.json())
    return response.json()


@router.delete(
    "/task/{task_id}/link/{links_to}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task_link(task_id: str, links_to: str, token: str | None = None):
    validate_token(token)
    url = f"{URL}/task/{str(task_id)}/link/{str(links_to)}"
    response = requests.delete(url, headers=header(token=token))
    if not response.status_code < 400:
        raise HTTPException(response.status_code, response.json())
    return response.json()


@router.delete("/task/{task_id}/dependency", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_dependency(
    task_id: str,
    depends_on: str | None = Query(
        default=None, description="ID of the task", examples=[None]
    ),
    dependency_of: str | None = Query(
        default=None, description="ID of the task", examples=[None]
    ),
    token: str | None = None,
):
    validate_token(token)
    url = f"{URL}/task/{str(task_id)}/dependency"

    query = {"depends_on": depends_on, "dependency_of": dependency_of}

    response = requests.delete(
        url, params=query, headers=header(token=token, content_type="application/json")
    )
    if not response.status_code < 400:
        raise HTTPException(response.status_code, response.json())
    return response.json()
