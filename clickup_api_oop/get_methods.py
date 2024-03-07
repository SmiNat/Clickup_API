from __future__ import annotations

import datetime

import requests
from dotenv import load_dotenv

from clickup_api.handlers import (
    check_and_adjust_list_length,
    check_boolean,
    check_integer_list,
    datetime_to_unix_time_in_milliseconds,
)

from .main import ClickUpAPI

load_dotenv()


class ClickUpGETMethods(ClickUpAPI):
    """Methods for GET requests in ClickUp API."""

    # def __init__(self, token: str, api_url: str | None = None) -> None:
    #     super().__init__(token, api_url)

    def get_authorized_user(
        self, as_json: bool = True, token: str | None = None
    ) -> dict | requests.Response:
        """
        Execute GET request to view the details of the authenticated user's ClickUp account.
        More info: https://clickup.com/api/clickupreference/operation/GetAuthorizedUser/

        Args:
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "user/"

        response = requests.get(url, headers=self.header(token=token))
        return response.json() if as_json else response

    def get_authorized_teams_workspaces(
        self, as_json: bool = True, token: str | None = None
    ) -> dict | requests.Response:
        """Execute GET request to view the Workspaces available to the authenticated user.
        More info: https://clickup.com/api/clickupreference/operation/GetAuthorizedTeams/

        Args:
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance.  Defaults to None.
        Returns:
            dict | Any:Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "team/"

        response = requests.get(url, headers=self.header(token=token))
        return response.json() if as_json else response

    def get_teams(
        self,
        team_id: int | None = None,
        group_ids: str | None = None,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute GET request to view Teams: user groups in a Workspace.
        More info: https://clickup.com/api/clickupreference/operation/GetTeams1/
        Additional info: https://help.clickup.com/hc/en-us/articles/6326036524823-Create-user-groups-with-Teams

        Args:
            team_id (int | None, optional): ID of a Workspace. Defaults to None.
            group_ids (str | None, optional): ID(s) of a user group. Defaults to None.
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "group"

        query = {"team_id": team_id, "group_ids": group_ids}

        response = requests.get(url, headers=self.header(token=token), params=query)
        return response.json() if as_json else response

    def get_spaces(
        self, team_id: int, as_json: bool = True, token: str | None = None
    ) -> dict | requests.Response:
        """
        Execute GET request to view Spaces available in a Workspace.
        More info: https://clickup.com/api/clickupreference/operation/GetSpaces//

        Args:
            team_id (int): Team ID (Workspace).
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "team/" + str(team_id) + "/space"

        response = requests.get(url, headers=self.header(token=token))
        return response.json() if as_json else response

    def get_space(
        self, space_id: int, as_json: bool = True, token: str | None = None
    ) -> dict | requests.Response:
        """
        Execute GET request to view the Spaces available in a Workspace.
        More info: https://clickup.com/api/clickupreference/operation/GetSpace/

        Args:
            space_id (int)
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "space/" + str(space_id)

        response = requests.get(url, headers=self.header(token=token))
        return response.json() if as_json else response

    def get_folders(
        self,
        space_id: int,
        archived: bool = False,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute GET request to view Folders in a Space.
        More info: https://clickup.com/api/clickupreference/operation/GetFolders/

        Args:
            space_id (int)
            archived (bool): If True, returns response of archived data. \
                Defaults to False.
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "space/" + str(space_id) + "/folder"

        query = {
            "archived": "true" if check_boolean(archived) else "false",
        }

        response = requests.get(url, headers=self.header(token=token), params=query)
        return response.json() if as_json else response

    def get_folder(
        self,
        folder_id: int,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute GET request to view the Lists within a Folder.
        More info: https://clickup.com/api/clickupreference/operation/GetFolder/

        Args:
            folder_id (int)
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "folder/" + str(folder_id)

        response = requests.get(url, headers=self.header(token=token))
        return response.json() if as_json else response

    def get_lists(
        self,
        folder_id: int,
        archived: bool = False,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute GET request to view Lists within a Folder.
        More info: https://clickup.com/api/clickupreference/operation/GetLists/

        Args:
            folder_id (int): ID of a Folder.
            archived (bool, optional): If True, returns response of archived data. \
                Defaults to False.
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "folder/" + str(folder_id) + "/list"

        query = {
            "archived": "true" if archived else "false",
        }

        response = requests.get(url, headers=self.header(token=token), params=query)
        return response.json() if as_json else response

    def get_list(
        self,
        list_id: int,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute GET request to view information about a List.
        More info: https://clickup.com/api/clickupreference/operation/GetList/

        Args:
            list_id (int)
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "list/" + str(list_id)

        response = requests.get(url, headers=self.header(token=token))
        return response.json() if as_json else response

    def get_folderless_lists(
        self,
        space_id: int,
        archived: bool = False,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute GET request to view the Lists in a Space that aren't located in a Folder.
        More info: https://clickup.com/api/clickupreference/operation/GetFolderlessLists/

        Args:
            space_id (int)
            archived (bool, optional):  If True, returns response of archived data. \
                Defaults to False.
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "space/" + str(space_id) + "/list"

        query = {
            "archived": "true" if archived else "false",
        }

        response = requests.get(url, headers=self.header(token=token), params=query)
        return response.json() if as_json else response

    def get_tasks(
        self,
        list_id: int,
        archived: bool = False,
        include_markdown_description: bool = False,
        page: int = 0,
        order_by: str = "created",
        reverse: bool = False,
        subtasks: bool = False,
        statuses: list[str] | None = None,
        include_closed: bool = False,
        assignees: list[int | str] | None = None,
        tags: list[str] | None = None,
        due_date_gt: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        due_date_lt: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        date_created_gt: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        date_created_lt: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        date_updated_gt: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        date_updated_lt: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        date_done_gt: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        date_done_lt: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        custom_fields: list[str] | None = None,  # NotImplemented
        custom_items: list[int] | None = None,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute GET request to view Tasks in a List. Responses are limited to 100 tasks per page.
        You can only view task information of tasks you can access.
        This endpoint only includes tasks where the specified list_id is their home List.
        Tasks added to the list_id with a different home List are not included in the response.
        More info: https://clickup.com/api/clickupreference/operation/GetTasks/
        For filtering tasks using custom fields: https://clickup.com/api/developer-portal/filtertasks/

        Args:
            list_id (int): ID of a List.
            archived (bool, optional): If True, returns response of archived data. \
                Defaults to False.
            include_markdown_description (bool, optional): Return task descriptions \
                in Markdown format. Defaults to False.
            page (int, optional): Page to fetch. Defaults to  0.
            order_by (str, optional): Order by a particular field. By default, \
                tasks are ordered by created. Options include: id, created, updated, \
                and due_date.
            reverse (bool, optional): Tasks are displayed in reverse order. \
                Defaults to False.
            subtasks (bool, optional): Include or exclude subtasks. By default, \
                subtasks are excluded.
            statuses (list[str] | None, optional): Filter by statuses. Defaults to None. \
                List of available statuses: see 'available_statuses' class attribute.
            include_closed (bool, optional): Include or excluse closed tasks. \
                By default, they are excluded. {}
            assignees (list[int | str] | None, optional): Filter by Assignees. \
                Defaults to None.
            tags (list[str] | None, optional): ilter by Tags. Defaults to None.
            due_date_gt (datetime.datetime | list[int] | tuple[int] | None, optional):\
                Filter by due date greater than Unix time in milliseconds. \
                Use datetime.datetime() to set a due_date_gt. \
                Alternatively type due_date_gt as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            due_date_lt (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Filter by due date greater than Unix time in milliseconds. \
                Use datetime.datetime() to set a due_date_lt. \
                Alternatively type due_date_lt as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            date_created_gt (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Filter by due date greater than Unix time in milliseconds. \
                Use datetime.datetime() to set a date_created_gt. \
                Alternatively type date_created_gt as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            date_created_lt (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Filter by due date greater than Unix time in milliseconds. \
                Use datetime.datetime() to set a date_created_lt. \
                Alternatively type date_created_lt as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            date_updated_gt (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Filter by due date greater than Unix time in milliseconds. \
                Use datetime.datetime() to set a date_updated_gt. \
                Alternatively type date_updated_gt as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            date_updated_lt (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Filter by due date greater than Unix time in milliseconds. \
                Use datetime.datetime() to set a date_updated_lt. \
                Alternatively type date_updated_lt as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            date_done_gt (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Filter by due date greater than Unix time in milliseconds. \
                Use datetime.datetime() to set a date_done_gt. \
                Alternatively type date_done_gt as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            date_done_lt (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Filter by due date greater than Unix time in milliseconds. \
                Use datetime.datetime() to set a date_done_lt. \
                Alternatively type date_done_lt as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            custom_fields (list[str] | None, optional):  Include tasks with specific \
                values in one or more Custom Fields.  Defaults to None. Note: Not Implemented.
            custom_items (list[int] | None, optional): Filter by custom task types. \
                Defaults to None. Icluding 0 returns tasks. Including 1 returns \
                Milestones. Including any other number returns the custom task type \
                as defined in your Workspace.
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "list/" + str(list_id) + "/task"

        if not isinstance(order_by, str):
            raise TypeError("Invalid 'order_by' type. 'order_by' must be a string.")
        if order_by not in ["id", "created", "updated", "due_date"]:
            raise ValueError(
                "Invalid 'order_by' field choice. Allowed choices are: "
                "'id', 'created', 'updated', 'due_date'."
            )

        if custom_fields:
            raise NotImplementedError(
                "A 'custom_fields' functionality is not yet implemented."
            )

        query = {
            "archived": "true" if check_boolean(archived) else "false",
            "include_markdown_description": (
                "true" if check_boolean(include_markdown_description) else "false"
            ),
            "page": page,
            "order_by": order_by,
            "reverse": "true" if check_boolean(reverse) else "false",
            "subtasks": "true" if check_boolean(subtasks) else None,
            "statuses": check_and_adjust_list_length(statuses),
            "include_closed": "true" if check_boolean(include_closed) else "false",
            "assignees": check_and_adjust_list_length(assignees),
            "tags": check_and_adjust_list_length(tags),
            "due_date_gt": (
                datetime_to_unix_time_in_milliseconds(due_date_gt)
                if due_date_gt
                else due_date_gt
            ),
            "due_date_lt": (
                datetime_to_unix_time_in_milliseconds(due_date_lt)
                if due_date_lt
                else due_date_lt
            ),
            "date_created_gt": (
                datetime_to_unix_time_in_milliseconds(date_created_gt)
                if date_created_gt
                else date_created_gt
            ),
            "date_created_lt": (
                datetime_to_unix_time_in_milliseconds(date_created_lt)
                if date_created_lt
                else date_created_lt
            ),
            "date_updated_gt": (
                datetime_to_unix_time_in_milliseconds(date_updated_gt)
                if date_updated_gt
                else date_updated_gt
            ),
            "date_updated_lt": (
                datetime_to_unix_time_in_milliseconds(date_updated_lt)
                if date_updated_lt
                else date_updated_lt
            ),
            "date_done_gt": (
                datetime_to_unix_time_in_milliseconds(date_done_gt)
                if date_done_gt
                else date_done_gt
            ),
            "date_done_lt": (
                datetime_to_unix_time_in_milliseconds(date_done_lt)
                if date_done_lt
                else date_done_lt
            ),
            "custom_fields": custom_fields,
            "custom_items": (
                check_integer_list(custom_items) if custom_items else custom_items
            ),
        }

        response = requests.get(url, headers=self.header(token=token), params=query)
        return response.json() if as_json else response

    def get_task(
        self,
        task_id: str,
        custom_task_ids: bool = False,
        team_id: int | None = None,
        include_subtasks: bool = False,
        include_markdown_description: bool = False,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute GET request to view information about a task.
        You can only view task information of tasks you can access.
        Tasks with attachments will return an "attachments" response.
        More info: https://clickup.com/api/clickupreference/operation/GetTask/

        Args:
            task_id (str): ClickUp task id.
            custom_task_ids (bool): If you want to reference a task by it's custom \
                task ID, this value must be set to True. Defaults to False.
            team_id (int | None, optional): Only used when the custom_task_ids \
                parameter is set to True. Defaults to None.
            include_subtasks (bool): Include subtasks. Defaults to False.
            include_markdown_description (bool): Return task descriptions in \
                Markdown format. Defaults to False.
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "task/" + str(task_id)

        custom_task_ids = "true" if team_id or custom_task_ids else "false"

        query = {
            "custom_task_ids": custom_task_ids,
            "team_id": team_id,
            "include_subtasks": (
                "true" if check_boolean(include_subtasks) else "false"
            ),
            "include_markdown_description": (
                "true" if check_boolean(include_markdown_description) else "false"
            ),
        }

        response = requests.get(url, headers=self.header(token=token), params=query)
        return response.json() if as_json else response

    def get_user(
        self, team_id: int, user_id: int, as_json: bool = True, token: str | None = None
    ) -> dict | requests.Response:
        """
        Execute GET request to view information about a user in a Workspace.
        Note: This endpoint is only available to Workspaces on Enterprise Plan.
        More info: https://clickup.com/api/clickupreference/operation/GetUser/

        Args:
            team_id (int): Team ID (Workspace).
            user_id (int): User ID.
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "team/" + str(team_id) + "/user/" + str(user_id)

        response = requests.get(url, headers=self.header(token=token))
        return response.json() if as_json else response

    def get_time_entries(
        self,
        team_id: int,
        start_date: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        end_date: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        assignee: int | list[int] | tuple[int] | None = None,
        include_task_tags: bool = False,
        include_location_names: bool = False,
        space_id: int | None = None,
        folder_id: int | None = None,
        list_id: int | None = None,
        task_id: str | None = None,
        custom_task_ids: bool = False,
        query_team_id: int | None = None,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute GET request to view time entries filtered by start and end date.
        By default, this endpoint returns time entries from beginning of the current
        month till now created by the authenticated user.
        To retrieve time entries for other users, you must include the assignee query parameter.
        Only one of the following location filters can be included at a time:
        space_id, folder_id, list_id, or task_id.
        Note: A time entry that has a negative duration means that timer is currently
        running for that user.
        Note: Content-Type as "application/json" implemented as required by the ClickUp API.
        More info: https://clickup.com/api/clickupreference/operation/Gettimeentrieswithinadaterange/

        Args:
            team_id (int): Team ID (Workspace).
            start_date (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Sets beginning of a time search. If None, equals to the beginning of \
                the current month. Use datetime.datetime() to set a start_date. \
                Alternatively type start_date as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            end_date (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Sets end of a time search. If None, equals to current date and time. \
                Use datetime.datetime() to set a end_date. \
                Alternatively type end_date as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            assignee (int | list[int] | tuple[int] | None, optional): \
                Filter time entries by user_id. Provide the user_id as an integer. \
                For multiple assignees, use list or tuple with user_id numbers. \
                Note: Only Workspace Owners/Admins have access to do this.
            include_task_tags (bool, optional): Include task tags in the response \
                for time entries associated with tasks. Defaults to False.
            include_location_names (bool, optional): Include the names of the List, \
                Folder, and Space along with the list_id, folder_id, and space_id. \
                    Defaults to False.
            space_id (int | None, optional): Only include time entries associated \
                with tasks in a specific Space. Defaults to None.
            folder_id (int | None, optional): Only include time entries associated \
                with tasks in a specific Folder. Defaults to None.
            list_id (int | None, optional): Only include time entries associated \
                with tasks in a specific List. Defaults to None.
            task_id (str | None, optional):  Only include time entries associated \
                with a specific task. Defaults to None.
            custom_task_ids (bool, optional): If you want to reference a task by \
                it's custom task ID, this value  must be set to True. Defaults to False.
            query_team_id (int | None, optional): Only used when the custom_task_ids \
                parameter is set to True. Defaults to None.
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "team/" + str(team_id) + "/time_entries"

        if start_date:
            start_date = datetime_to_unix_time_in_milliseconds(start_date)
        else:
            start_date = datetime_to_unix_time_in_milliseconds(
                datetime.datetime(
                    datetime.date.today().year, datetime.date.today().month, 1
                )
            )
        if end_date:
            end_date = datetime_to_unix_time_in_milliseconds(end_date)
        else:
            end_date = datetime_to_unix_time_in_milliseconds(datetime.datetime.now())

        if assignee:
            if isinstance(assignee, str):
                try:
                    assignee = int(assignee)
                except TypeError:
                    raise TypeError(
                        "Invalid assignee ID. For a single user ID type ID "
                        "as an integer number."
                    )

            if not isinstance(assignee, (int, list, tuple)):
                raise TypeError(
                    "Invalid assignee ID(s). For a single user type ID as a integer number. "
                    "For multiple users use list or tuple of integer numbers."
                )

            if isinstance(assignee, int):
                user_ids = assignee
            else:
                user_ids = ",".join(str(element) for element in assignee)

        custom_task_ids = (
            "true" if (query_team_id or check_boolean(custom_task_ids)) else "false"
        )

        query = {
            "start_date": start_date,
            "end_date": end_date,
            "assignee": assignee if not assignee else str(user_ids),
            "include_task_tags": (
                "true" if check_boolean(include_task_tags) else "false"
            ),
            "include_location_names": (
                "true" if check_boolean(include_location_names) else "false"
            ),
            "space_id": space_id,
            "folder_id": folder_id,
            "list_id": list_id,
            "task_id": task_id,
            "custom_task_ids": custom_task_ids,
            "team_id": query_team_id,
        }

        response = requests.get(
            url,
            headers=self.header(content_type="application/json", token=token),
            params=query,
        )
        return response.json() if as_json else response

    def get_task_comments(
        self,
        task_id: str,
        custom_task_ids: bool = False,
        team_id: int | None = None,
        start: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        start_id: str | None = None,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute GET request to view task comments.
        If the 'start' and 'start_id' parameters are not included, this endpoint will
        return the most recent 25 comments. Use the 'start' and 'start_id' parameters
        of the oldest comment to retrieve the next 25 comments.
        More info: https://clickup.com/api/clickupreference/operation/GetTaskComments/

        Args:
            task_id (str): ID of a task.
            custom_task_ids (bool, optional): If you want to reference a task by \
                it's custom task ID, this value must be set to True. Defaults to False.
            team_id (int | None, optional): Team ID (Workspace). Only used when \
                the custom_task_ids parameter is set to true. Defaults to None.
            start (datetime.datetime | list[int] | tuple[int] | None, optional): \
                The date of task comment. Use datetime.datetime() to set a start. \
                Alternatively type start as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            start_id (str | None, optional): Enter the Comment id of a task comment. \
                Defaults to None.
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "task/" + str(task_id) + "/comment"

        if start:
            start = datetime_to_unix_time_in_milliseconds(start)

        query = {
            "custom_task_ids": (
                "true" if check_boolean(custom_task_ids) or team_id else "false"
            ),
            "team_id": team_id,
            "start": start,
            "start_id": start_id,
        }

        response = requests.get(url, headers=self.header(token=token), params=query)
        return response.json() if as_json else response

    def get_list_comments(
        self,
        list_id: int,
        start: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        start_id: str | None = None,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute GET request to view the comments added to a List.
        If the 'start' and 'start_id' parameters are not included, this endpoint will
        return the most recent 25 comments. Use the 'start' and 'start_id' parameters
        of the oldest comment to retrieve the next 25 comments.
        More info: https://clickup.com/api/clickupreference/operation/GetListComments/

        Args:
            list_id (int): ID of a List.
            start (datetime.datetime | list[int] | tuple[int] | None, optional): \
                The date of task comment. Use datetime.datetime() to set a start. \
                Alternatively type start as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            start_id (str | None, optional): Enter the Comment id of a task comment.\
                Defaults to None.
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "list/" + str(list_id) + "/comment"

        if start:
            start = datetime_to_unix_time_in_milliseconds(start)

        query = {
            "start": start,
            "start_id": start_id,
        }

        response = requests.get(url, headers=self.header(token=token), params=query)
        return response.json() if as_json else response

    def get_chat_view_comments(
        self,
        view_id: str,
        start: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        start_id: str | None = None,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute GET request to view comments from a Chat view.
        If the 'start' and 'start_id' parameters are not included, this endpoint will
        return the most recent 25 comments. Use the 'start' and 'start_id' parameters
        of the oldest comment to retrieve the next 25 comments.
        More info: https://clickup.com/api/clickupreference/operation/GetChatViewComments/

        Args:
            view_id (str): ID of a View.
            start (datetime.datetime | list[int] | tuple[int] | None, optional): \
                The date of task comment. Use datetime.datetime() to set a start. \
                Alternatively type start as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            start_id (str | None, optional): Enter the Comment id of a task comment. \
                Defaults to None.
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "view/" + str(view_id) + "/comment"

        if start:
            start = datetime_to_unix_time_in_milliseconds(start)

        query = {
            "start": start,
            "start_id": start_id,
        }

        response = requests.get(url, headers=self.header(token=token), params=query)
        return response.json() if as_json else response

    def get_custom_task_types(
        self, team_id: str, as_json: bool = True, token: str | None = None
    ) -> dict | requests.Response:
        """
        Execute GET request to view the custom task types available in a Workspace.
        More info: https://clickup.com/api/clickupreference/operation/GetCustomItems/

        Args:
            team_id (str): Team ID (Workspace)
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "team/" + str(team_id) + "/custom_item"

        response = requests.get(url, headers=self.header(token=token))
        return response.json() if as_json else response

    def get_accessible_custom_fields(
        self, list_id: str, as_json: bool = True, token: str | None = None
    ) -> dict | requests.Response:
        """
        Execute GET request to view the Custom Fields available on tasks in a specific List.
        More info: https://clickup.com/api/clickupreference/operation/GetAccessibleCustomFields/

        Args:
            list_id (int): ID of a List.
            as_json (bool, optional): If True, returns response as a JSON type. \
                Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "list/" + str(list_id) + "/field"

        response = requests.get(
            url, headers=self.header(content_type="application/json", token=token)
        )
        return response.json() if as_json else response
