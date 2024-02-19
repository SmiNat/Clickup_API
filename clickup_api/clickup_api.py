from __future__ import annotations
from typing import Any
from dotenv import load_dotenv
from urllib.parse import urlparse
import datetime
import random
import requests
import string

from .enums import ClickupActions
from .exceptions import DateSequenceError, DateTypeError, DateDataError


load_dotenv()


class ClickUpAPI:
    """A class to handle ClickUp API."""

    _API_DEFAULT_URL = "https://app.clickup.com/api/v2/"
    available_statuses = [
        "nowe",
        "w trakcie",
        "oczekujące",
        "odrzucone",
        "gotowe",
        "zamknięte",
    ]

    def __init__(self, token: str, api_url: str | None = None) -> None:
        """Constructs attributes for authorization in ClickUp API and validates url address.

        Args:
            token (str):
                Token for authentication via ClickUp API.
            clickup_api_url (str, optional):
                Official URL address for ClickUp API.
                If None, defaults to "https://app.clickup.com/api/v2/".
        Raises:
            ValueError: Raises Invalid URL address.
        Returns:
            None
        """

        self.token = token
        self.api_url = api_url

    def __repr__(self) -> str:
        """Class representation."""
        return (
            f"{self.__class__.__name__}(api_url='{self.api_url}', token={self.token})"
        )

    @classmethod
    def change_available_status(
        cls, status_name: str, action: str = ClickupActions.ADD
    ) -> None:
        """Updates list of available statuses. Acceptable action is 'add' or 'remove'."""
        if action not in list(map(lambda c: c.value, ClickupActions)):
            raise ValueError(
                "Invalid action type. Acceptable actions are: 'add' or 'remove'."
            )
        if action == ClickupActions.ADD and status_name not in cls.available_statuses:
            cls.available_statuses.append(status_name)
        elif action == ClickupActions.REMOVE and status_name in cls.available_statuses:
            cls.available_statuses.remove(status_name)

    @staticmethod
    def is_url(url: str) -> bool:
        """Validates url address."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    @staticmethod
    def check_token(token: str) -> None:
        """Validates token."""
        if not isinstance(token, str):
            raise TypeError(f"Token must be of type: str, not {type(token)}.")
        if isinstance(token, str) and len(token) == 0:
            raise ValueError("Empty string is not allowed.")

    @staticmethod
    def check_positive_integer(value: int) -> None:
        """Validates if argument is a positive integer."""
        if not isinstance(value, int):
            raise TypeError(f"'{value}' must be an integer, not {type(value)} type.")
        if isinstance(value, int) and value < 0:
            raise ValueError("Only positive number is allowed.")

    @staticmethod
    def check_integer_list(data: list[int]) -> None:
        """Validates if data is a list of integers."""
        if not isinstance(data, list):
            raise TypeError(f"'{data}' must be a list, not {type(data)} type.")
        for element in data:
            if not isinstance(element, int):
                raise TypeError("All list items must be integers.")

    @staticmethod
    def check_boolean(value: bool) -> bool:
        """Validates if value is a boolean."""
        if not isinstance(value, bool):
            raise TypeError(f"'{value}' must be of type: boolean, not {type(value)}.")
        return value

    @staticmethod
    def datetime_to_unix_time_in_milliseconds(
        date: datetime.datetime | list[int] | tuple[int],
    ) -> int:
        """Converts datetime.date or date represented by list of [year, month, day] or
        tuple of (year, month day) to unix time in milliseconds."""
        if date:
            if isinstance(date, datetime.datetime):
                date = int(date.timestamp() * 1000)
            elif isinstance(date, (list, tuple)) and len(date) >= 3 and len(date) <= 6:
                try:
                    date = int(datetime.datetime(*date).timestamp() * 1000)
                except ValueError as error:
                    raise DateSequenceError(error)
                except TypeError as error:
                    raise DateTypeError(error)
            else:
                raise DateDataError()
        return date

    @staticmethod
    def check_and_adjust_list_length(data: list, append_number: bool = False) -> list:
        """Validates if type of data is a list. If a list contains only one element,
        appends either random string or random number.
        Args:
            data (list):
                Array of strings or array of numbers as required for query parameter in ClickUp API.
            append_number (bool, optional):
                If True appends to a list random 8-digit number.
                If False appends to a list random 8-character string. Defaults to False.
                Only executes when the length of the data in a list is one.
        Raises:
            TypeError: Raises Invalid data type error.
        Returns:
            list:
                Returns a list of minimum two elements or an empty list.
        """
        if data:
            if not isinstance(data, list):
                raise TypeError("Invalid data type. Only 'list' of strings is allowed.")
            if len(data) == 1:
                if append_number:
                    random_value = int("".join(random.choices(string.digits, k=8)))
                else:
                    random_value = "".join(
                        random.choices(string.ascii_letters + string.digits, k=8)
                    )
                data.append(random_value)
        return data

    @property
    def token(self) -> str:
        """Returns token."""
        return str(self._token)

    @token.setter
    def token(self, new_token: str) -> None:
        """Sets a new token."""
        self.check_token(new_token)
        self._token = str(new_token)

    @property
    def api_url(self) -> str:
        """Returns ClickUp API main url."""
        return str(self._api_url)

    @api_url.setter
    def api_url(self, url: str) -> None:
        """Sets new ClickUp API url."""
        if url is None:
            self._api_url = self._API_DEFAULT_URL
        elif not isinstance(url, str):
            raise TypeError(f"Invalid URL type. URL address must be a string.")
        elif not self.is_url(url):
            raise ValueError("'{url}' is not a valid URL address.")
        elif url.endswith("/"):
            self._api_url = url
        else:
            self._api_url = url + "/"

    def header(
        self, content_type: str = "application/json", token: str | None = None
    ) -> dict[str, str]:
        """Sets the type of content for a given request.

        Args:
            content_type (str, optional):
                Type of request content. Defaults to "application/json".
            token (str | None, optional):
                Token for request authentication. If None, uses token of an instance.
                Defaults to None.
        Returns:
            dict[str, str]: Content for a request header.
        """

        if not token:
            api_key = str(self._token)
        else:
            self.check_token(token)
            api_key = str(token)
        request_header = {"Authorization": api_key, "Content-Type": content_type}
        return request_header


class ClickUpGETMethods(ClickUpAPI):
    """Methods for GET requests in ClickUp API."""

    def __init__(self, token: str, api_url: str | None = None) -> None:
        super().__init__(token, api_url)

    def get_authorized_teams_workspaces(
        self, as_json: bool = True, token: str | None = None
    ) -> dict | requests.Response:
        """Execute GET request to view the Workspaces available to the authenticated user.
        More info: https://clickup.com/api/clickupreference/operation/GetAuthorizedTeams/

        Args:
            as_json (bool, optional):
                If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional):
                Token for request authentication. If None, uses token of an instance.
                Defaults to None.
        Returns:
            dict | Any:
                Returns response either as a class 'requests.models.Response' or
                as a JSON dictionary.
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
            team_id (int | None, optional):
                ID of a Workspace. Defaults to None.
            group_ids (str | None, optional):
                ID(s) of a user group. Defaults to None.
            as_json (bool, optional):
                If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional):
                Token for request authentication. If None, uses token of an instance.
                Defaults to None.
        Returns:
            dict | Any:
                Returns response either as a class 'requests.models.Response' or
                as a JSON dictionary.
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
            team_id (int):
                Team ID (Workspace).
            as_json (bool, optional):
                If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional):
                Token for request authentication. If None, uses token of an instance.
                Defaults to None.
        Returns:
            dict | Any:
                Returns response either as a class 'requests.models.Response' or
                as a JSON dictionary.
        """

        url = self.api_url + "team/" + str(team_id) + "/space"

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
            space_id (int):
                ID of a Space.
            archived (bool, optional):
                If True, returns response of archived data. Defaults to False
            as_json (bool, optional):
                If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional):
                Token for request authentication. If None, uses token of an instance.
                Defaults to None.
        Returns:
            dict | Any:
                Returns response either as a class 'requests.models.Response' or
                as a JSON dictionary.
        """

        url = self.api_url + "space/" + str(space_id) + "/folder"

        query = {
            "archived": "true" if self.check_boolean(archived) else "false",
        }

        response = requests.get(url, headers=self.header(token=token), params=query)
        return response.json() if as_json else response

    def get_lists(
        self,
        folder_id: int,
        archived: bool = False,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute GET request to view Lists wuthin a Folder.
        More info: https://clickup.com/api/clickupreference/operation/GetLists/

        Args:
            folder_id (int):
                ID of a Folder.
            archived (bool, optional):
                If True, returns response of archived data. Defaults to False.
            as_json (bool, optional):
                If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional):
                Token for request authentication. If None, uses token of an instance.
                Defaults to None.
        Returns:
            dict | Any:
                Returns response either as a class 'requests.models.Response' or
                as a JSON dictionary.
        """

        url = self.api_url + "folder/" + str(folder_id) + "/list"

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
            list_id (int):
                ID of a List.
            archived (bool, optional):
                If True, returns response of archived data. Defaults to False.
            include_markdown_description (bool, optional):
                Return task descriptions in Markdown format. Defaults to False.
            page (int, optional):
                Page to fetch. Defaults to  0.
            order_by (str, optional):
                Order by a particular field. By default, tasks are ordered by created.
                Options include: id, created, updated, and due_date.
            reverse (bool, optional):
                Tasks are displayed in reverse order. Defaults to False.
            subtasks (bool, optional):
                Include or exclude subtasks. By default, subtasks are excluded.
            statuses (list[str] | None, optional):
                Filter by statuses. Defaults to None.
                List of available statuses: see 'available_statuses' class attribute.
            include_closed (bool, optional):
                Include or excluse closed tasks. By default, they are excluded. {}
            assignees (list[int | str] | None):
                Filter by Assignees. Defaults to None.
            tags (list[str] | None):
                Filter by Tags. Defaults to None.
            due_date_gt (datetime.datetime | list[int] | tuple[int] | None, optional):
                Filter by due date greater than Unix time in milliseconds.
                Use datetime.datetime() to set a due_date_gt.
                Alternatively type due_date_gt as a list or a tuple of integer values
                in the following order: (year, month, day[, hour, minute, second]).
                Defaults to None.
            due_date_lt (datetime.datetime | list[int] | tuple[int] | None, optional):
                Filter by due date greater than Unix time in milliseconds.
                Use datetime.datetime() to set a due_date_lt.
                Alternatively type due_date_lt as a list or a tuple of integer values
                in the following order: (year, month, day[, hour, minute, second]).
                Defaults to None.
            date_created_gt (datetime.datetime | list[int] | tuple[int] | None, optional):
                Filter by due date greater than Unix time in milliseconds.
                Use datetime.datetime() to set a date_created_gt.
                Alternatively type date_created_gt as a list or a tuple of integer values
                in the following order: (year, month, day[, hour, minute, second]).
                Defaults to None.
            date_created_lt (datetime.datetime | list[int] | tuple[int] | None, optional):
                Filter by due date greater than Unix time in milliseconds.
                Use datetime.datetime() to set a date_created_lt.
                Alternatively type date_created_lt as a list or a tuple of integer values
                in the following order: (year, month, day[, hour, minute, second]).
                Defaults to None.
            date_updated_gt (datetime.datetime | list[int] | tuple[int] | None, optional):
                Filter by due date greater than Unix time in milliseconds.
                Use datetime.datetime() to set a date_updated_gt.
                Alternatively type date_updated_gt as a list or a tuple of integer values
                in the following order: (year, month, day[, hour, minute, second]).
                Defaults to None.
            date_updated_lt (datetime.datetime | list[int] | tuple[int] | None, optional):
                Filter by due date greater than Unix time in milliseconds.
                Use datetime.datetime() to set a date_updated_lt.
                Alternatively type date_updated_lt as a list or a tuple of integer values
                in the following order: (year, month, day[, hour, minute, second]).
                Defaults to None.
            date_done_gt (datetime.datetime | list[int] | tuple[int] | None, optional):
                Filter by due date greater than Unix time in milliseconds.
                Use datetime.datetime() to set a date_done_gt.
                Alternatively type date_done_gt as a list or a tuple of integer values
                in the following order: (year, month, day[, hour, minute, second]).
                Defaults to None.
            date_done_lt (datetime.datetime | list[int] | tuple[int] | None, optional):
                Filter by due date greater than Unix time in milliseconds.
                Use datetime.datetime() to set a date_done_lt.
                Alternatively type date_done_lt as a list or a tuple of integer values
                in the following order: (year, month, day[, hour, minute, second]).
                Defaults to None.
            custom_fields (list[str] | None, optional):
                Include tasks with specific values in one or more Custom Fields.
                Defaults to None. Note: Not Implemented.
            custom_items (list[int] | None, optional):
                Filter by custom task types. Defaults to None.
                Including 0 returns tasks. Including 1 returns Milestones.
                Including any other number returns the custom task type as defined in your Workspace.
            as_json (bool, optional):
                If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional):
                Token for request authentication. If None, uses token of an instance.
                Defaults to None.
        Returns:
            dict | Any:
                Returns response either as a class 'requests.models.Response' or
                as a JSON dictionary.
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
            "archived": "true" if self.check_boolean(archived) else "false",
            "include_markdown_description": (
                "true" if self.check_boolean(include_markdown_description) else "false"
            ),
            "page": page,
            "order_by": order_by,
            "reverse": "true" if self.check_boolean(reverse) else "false",
            "subtasks": "true" if self.check_boolean(subtasks) else None,
            "statuses": self.check_and_adjust_list_length(statuses),
            "include_closed": "true" if self.check_boolean(include_closed) else "false",
            "assignees": self.check_and_adjust_list_length(assignees),
            "tags": self.check_and_adjust_list_length(tags),
            "due_date_gt": (
                self.datetime_to_unix_time_in_milliseconds(due_date_gt)
                if due_date_gt
                else due_date_gt
            ),
            "due_date_lt": (
                self.datetime_to_unix_time_in_milliseconds(due_date_lt)
                if due_date_lt
                else due_date_lt
            ),
            "date_created_gt": (
                self.datetime_to_unix_time_in_milliseconds(date_created_gt)
                if date_created_gt
                else date_created_gt
            ),
            "date_created_lt": (
                self.datetime_to_unix_time_in_milliseconds(date_created_lt)
                if date_created_lt
                else date_created_lt
            ),
            "date_updated_gt": (
                self.datetime_to_unix_time_in_milliseconds(date_updated_gt)
                if date_updated_gt
                else date_updated_gt
            ),
            "date_updated_lt": (
                self.datetime_to_unix_time_in_milliseconds(date_updated_lt)
                if date_updated_lt
                else date_updated_lt
            ),
            "date_done_gt": (
                self.datetime_to_unix_time_in_milliseconds(date_done_gt)
                if date_done_gt
                else date_done_gt
            ),
            "date_done_lt": (
                self.datetime_to_unix_time_in_milliseconds(date_done_lt)
                if date_done_lt
                else date_done_lt
            ),
            "custom_fields": custom_fields,
            "custom_items": (
                self.check_integer_list(custom_items) if custom_items else custom_items
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
            task_id (str):
                ClickUp task id.
            custom_task_ids (bool, optional):
                If you want to reference a task by it's custom task ID, this value
                must be set to True. Defaults to False.
            team_id (int | None, optional):
                Only used when the custom_task_ids parameter is set to True. Defaults to None.
            include_subtasks (bool, optional):
                Include subtasks. Defaults to False.
            include_markdown_description (bool, optional):
                Return task descriptions in Markdown format. Defaults to False.
            as_json (bool, optional):
                If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional):
                Token for request authentication. Defaults to None.
        Returns:
            dict | Any:
                Returns response either as a class 'requests.models.Response' or
                as a JSON dictionary.
        """

        url = self.api_url + "task/" + str(task_id)

        custom_task_ids = "true" if team_id or custom_task_ids else "false"

        query = {
            "custom_task_ids": custom_task_ids,
            "team_id": team_id,
            "include_subtasks": (
                "true" if self.check_boolean(include_subtasks) else "false"
            ),
            "include_markdown_description": (
                "true" if self.check_boolean(include_markdown_description) else "false"
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
            team_id (int):
                Team ID (Workspace).
            user_id (int):
                User ID.
            as_json (bool, optional):
                If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional):
                Token for request authentication. If None, uses token of an instance.
                Defaults to None.
        Returns:
            dict | Any:
                Returns response either as a class 'requests.models.Response' or
                as a JSON dictionary.
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
            team_id (int):
                Team ID (Workspace).
            start_date (datetime.datetime | list[int] | tuple[int] | None, optional):
                Sets beginning of a time search. If None, equals to the beginning of
                a current month. Use datetime.datetime() to set a start_date.
                Alternatively type start_date as a list or a tuple of integer values
                in the following order: (year, month, day[, hour, minute, second]).
                Defaults to None.
            end_date (datetime.datetime | list[int] | tuple[int] | None, optional):
                Sets end of a time search. If None, equals to current date and time.
                Use datetime.datetime() to set a end_date.
                Alternatively type end_date as a list or a tuple of integer values
                in the following order: (year, month, day[, hour, minute, second]).
                Defaults to None.
            assignee (int | list[int] | tuple[int] | None, optional):
                Filter time entries by user_id. Provide the user_id as an integer.
                For multiple assignees, use list or tuple with user_id numbers.
                Note: Only Workspace Owners/Admins have access to do this.
            include_task_tags (bool, optional):
                Include task tags in the response for time entries associated with tasks.
                Defaults to False.
            include_location_names (bool, optional):
                Include the names of the List, Folder, and Space along with
                the list_id, folder_id, and space_id. Defaults to False.
            space_id (int | None, optional):
                Only include time entries associated with tasks in a specific Space.
                Defaults to None.
            folder_id (int | None, optional):
                Only include time entries associated with tasks in a specific Folder.
                Defaults to None.
            list_id (int | None, optional):
                Only include time entries associated with tasks in a specific List.
                Defaults to None.
            task_id (str | None, optional):
                Only include time entries associated with a specific task. Defaults to None.
            custom_task_ids (bool, optional):
                If you want to reference a task by it's custom task ID, this value
                must be set to True. Defaults to False.
            query_team_id (int | None, optional):
                Only used when the custom_task_ids parameter is set to True. Defaults to None.
            as_json (bool, optional):
                If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional):
                Token for request authentication. If None, uses token of an instance.
                Defaults to None.
        Returns:
            dict | Any:
                Returns response either as a class 'requests.models.Response' or
                as a JSON dictionary.
        """

        url = self.api_url + "team/" + str(team_id) + "/time_entries"

        if start_date:
            start_date = self.datetime_to_unix_time_in_milliseconds(start_date)
        else:
            start_date = self.datetime_to_unix_time_in_milliseconds(
                datetime.datetime(
                    datetime.date.today().year, datetime.date.today().month, 1
                )
            )
        if end_date:
            end_date = self.datetime_to_unix_time_in_milliseconds(end_date)
        else:
            end_date = self.datetime_to_unix_time_in_milliseconds(
                datetime.datetime.now()
            )

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
            "true"
            if (query_team_id or self.check_boolean(custom_task_ids))
            else "false"
        )

        query = {
            "start_date": start_date,
            "end_date": end_date,
            "assignee": assignee if not assignee else str(user_ids),
            "include_task_tags": (
                "true" if self.check_boolean(include_task_tags) else "false"
            ),
            "include_location_names": (
                "true" if self.check_boolean(include_location_names) else "false"
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

    def get_authorized_user(
        self, as_json: bool = True, token: str | None = None
    ) -> dict | requests.Response:
        """
        Execute GET request to view the details of the authenticated user's ClickUp account.
        More info: https://clickup.com/api/clickupreference/operation/GetAuthorizedUser/

        Args:
            as_json (bool, optional):
                If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional):
                Token for request authentication. If None, uses token of an instance.
                Defaults to None.
        Returns:
            dict | Any:
                Returns response either as a class 'requests.models.Response' or
                as a JSON dictionary.
        """

        url = self.api_url + "user/"

        response = requests.get(url, headers=self.header(token=token))
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
            task_id (str):
                ID of a task.
            custom_task_ids (bool, optional):
                If you want to reference a task by it's custom task ID, this value
                must be set to True. Defaults to False.
            team_id (int | None, optional):
                Team ID (Workspace). Only used when the custom_task_ids parameter is
                set to true. Defaults to None.
            start (datetime.datetime | list[int] | tuple[int] | None, optional):
                The date of task comment. Use datetime.datetime() to set a start.
                Alternatively type start as a list or a tuple of integer values
                in the following order: (year, month, day[, hour, minute, second]).
                Defaults to None.
            start_id (str | None, optional):
                Enter the Comment id of a task comment. Defaults to None.
            as_json (bool, optional):
                If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional):
                Token for request authentication. If None, uses token of an instance.
                Defaults to None.
        Returns:
            dict | Any:
                Returns response either as a class 'requests.models.Response' or
                as a JSON dictionary.
        """

        url = self.api_url + "task/" + str(task_id) + "/comment"

        if start:
            start = self.datetime_to_unix_time_in_milliseconds(start)

        query = {
            "custom_task_ids": (
                "true" if self.check_boolean(custom_task_ids) or team_id else "false"
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
            list_id (int):
                ID of a List.
            start (datetime.datetime | list[int] | tuple[int] | None, optional):
                The date of task comment. Use datetime.datetime() to set a start.
                Alternatively type start as a list or a tuple of integer values
                in the following order: (year, month, day[, hour, minute, second]).
                Defaults to None.
            start_id (str | None, optional):
                Enter the Comment id of a task comment. Defaults to None.
            as_json (bool, optional):
                If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional):
                Token for request authentication. If None, uses token of an instance.
                Defaults to None.
        Returns:
            dict | Any:
                Returns response either as a class 'requests.models.Response' or
                as a JSON dictionary.
        """

        url = self.api_url + "list/" + str(list_id) + "/comment"

        if start:
            start = self.datetime_to_unix_time_in_milliseconds(start)

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
            view_id (str):
                ID of a View.
            start (datetime.datetime | list[int] | tuple[int] | None, optional):
                The date of task comment. Use datetime.datetime() to set a start.
                Alternatively type start as a list or a tuple of integer values
                in the following order: (year, month, day[, hour, minute, second]).
                Defaults to None.
            start_id (str | None, optional):
                Enter the Comment id of a task comment. Defaults to None.
            as_json (bool, optional):
                If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional):
                Token for request authentication. If None, uses token of an instance.
                Defaults to None.
        Returns:
            dict | Any:
                Returns response either as a class 'requests.models.Response' or
                as a JSON dictionary.
        """

        url = self.api_url + "view/" + str(view_id) + "/comment"

        if start:
            start = self.datetime_to_unix_time_in_milliseconds(start)

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
            team_id (str):
                Team ID (Workspace)
            as_json (bool, optional):
                If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional):
                Token for request authentication. If None, uses token of an instance.
                Defaults to None.
        Returns:
            dict | Any:
                Returns response either as a class 'requests.models.Response' or
                as a JSON dictionary.
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
            list_id (int):
                ID of a List.
            as_json (bool, optional):
                If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional):
                Token for request authentication. If None, uses token of an instance.
                Defaults to None.
        Returns:
            dict | Any:
                Returns response either as a class 'requests.models.Response' or
                as a JSON dictionary.
        """

        url = self.api_url + "list/" + str(list_id) + "/field"

        response = requests.get(
            url, headers=self.header(content_type="application/json", token=token)
        )
        return response.json() if as_json else response


class ClickUpAdditionalMethods(ClickUpGETMethods):

    def request_workspace_ids(
        self, team_id: Any | None = None, token: str | None = None
    ) -> list | tuple:
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
            workspaces = self.get_authorized_teams_workspaces(as_json=True, token=token)
            if not workspaces["teams"]:
                raise ValueError("No teams (workspaces) found for a given token.")
            teams = []
            for team in workspaces["teams"]:
                teams.append(team["id"])
        elif isinstance(team_id, (list, tuple)):
            teams = team_id
        else:
            raise TypeError(
                f"'team_id' must be a list or a tuple, not {type(team_id)}."
            )
        return teams

    def request_time_entries_for_workspace_ids(
        self, team_id: list[int] | tuple[int], **kwargs
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
            raise ValueError("'team_id' must be a list or a tuple with ID values.")

        responses = []
        for team in team_id:
            response = self.get_time_entries(team_id=team, as_json=True, **kwargs)
            if not "data" in response.keys():
                raise ReferenceError(
                    f"Request to access teams failed. ClickUp API error message: {response}."
                )
            else:
                responses.append(response)
        return responses

    def user_worktime(
        self,
        start_date: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        end_date: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        assignee: int | list[int] | tuple[int] | None = None,
        team_id: list[int] | tuple[int] | None = None,
        only_billable: bool = False,
        token: str | None = None,
    ) -> dict:
        """
        Returns a dictionary of usernames with their time tracked from time entries request.
        If no assignee, returns worktime for a token owner.

        Args:
            start_date (datetime.datetime | list[int] | tuple[int] | None, optional):
                Sets beginning of a time search. If None, equals to the beginning of
                a current month. Use datetime.datetime() to set a start_date.
                Alternatively type start_date as a list or a tuple of integer values
                in the following order: (year, month, day[, hour, minute, second]).
                Defaults to None.
            end_date (datetime.datetime | list[int] | tuple[int] | None, optional):
                Sets end of a time search. If None, equals to current date and time.
                Use datetime.datetime() to set a end_date.
                Alternatively type end_date as a list or a tuple of integer values
                in the following order: (year, month, day[, hour, minute, second]).
                Defaults to None.
            assignee (int | list[int] | tuple[int] | None, optional):
                Filter time entries by user_id. Provide the user_id as an integer.
                For multiple assignees, use a list or a tuple with user_id numbers.
                Note: Only Workspace Owners/Admins have access to do this.
            team_id (list[int] | tuple[int] | None, optional):
                Team ID (Workspace). Note: one user may be assigned to more than one team.
                For receiving worktime from multiple workspaces, type workspace IDs as
                a list or a tuple.
                If None, includes all teams available for token owner.
            only_billable (bool, optional):
                If set to True, calculates time tracked only of tasks with billable set
                to True. If False, returns all time tracked from time entries request.
                Defaults to False.
            token (str | None, optional):
                Token for request authentication. If None, uses token of an instance.
                Defaults to None.
        Returns:
            dict:
                Returns a dictionary of usernames with their time tracked from time
                entries request.
        """

        # select workspaces (team_ids) for user's work time - if there is no team_id
        # given as a parameter, take list of all available workspaces for a token owner

        workspaces = self.request_workspace_ids(team_id=team_id, token=token)

        time_entry_responses = self.request_time_entries_for_workspace_ids(
            workspaces,
            start_date=start_date,
            end_date=end_date,
            assignee=assignee,
            token=token,
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
                        duration_per_user[task["user"]["username"]] += int(
                            task["duration"]
                        )
                else:
                    if only_billable:
                        duration_per_user[task["user"]["username"]] = (
                            int(task["duration"]) if task["billable"] else 0
                        )
                    else:
                        duration_per_user[task["user"]["username"]] = int(
                            task["duration"]
                        )

        for user, duration in duration_per_user.items():
            duration_per_user[user] = str(
                datetime.timedelta(seconds=int(duration) / 1000)
            ).split(".")[0]

        return duration_per_user

    def user_tasks(
        self,
        username: str,
        start_date: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        end_date: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        team_id: list[int] | tuple[int] | None = None,
        token: str | None = None,
    ) -> dict:
        """
        Returns a dictionary with the user's tasks.
        If 'team_id' is None, returns users tasks from all workspaces identified for
        the given token.

        Args:
            username (str):
                Filter tasks by username (Name [Middle Name] Surname).
            start_date (datetime.datetime | list[int] | tuple[int] | None, optional):
                Sets beginning of a time search. If None, equals to the beginning of
                a current month. Use datetime.datetime() to set a start_date.
                Alternatively type start_date as a list or a tuple of integer values
                in the following order: (year, month, day[, hour, minute, second]).
                Defaults to None.
            end_date (datetime.datetime | list[int] | tuple[int] | None, optional):
                Sets end of a time search. If None, equals to current date and time.
                Use datetime.datetime() to set a end_date.
                Alternatively type end_date as a list or a tuple of integer values
                in the following order: (year, month, day[, hour, minute, second]).
                Defaults to None.
            team_id (list[int] | tuple[int] | None, optional):
                Team ID (Workspace). Note: one user may be assigned to more than one team.
                For receiving tasks from multiple workspaces, type workspace IDs as
                a list or a tuple. If None, includes all teams available for token owner.
                Defaults to None.
            token (str | None, optional):
                Token for request authentication. If None, uses token of an instance.
                Defaults to None.
        Returns:
            dict:
                Returns a dictionary of a username, a user_id and tasks (task_id,
                task_name and task total duration) for a selected user (assignee)
                in a given period of time.
        """

        workspaces_ids = self.request_workspace_ids(team_id=team_id, token=token)

        # for filtering by username and surname instead of user_id:
        workspaces_data = self.get_authorized_teams_workspaces(token=token)
        for team in workspaces_data["teams"]:
            is_user_in_workspace = False
            for user in team["members"]:
                if username == user["user"]["username"]:
                    assignee = user["user"][
                        "id"
                    ]  # getting user_id from username from workspace
                    is_user_in_workspace = True
                    break

        if not is_user_in_workspace:
            raise ValueError(
                f"User '{username}' not found in workspace list of members. "
                "Validate 'username' argument or use another token to search "
                "through different workspaces."
            )

        time_entry_responses = self.request_time_entries_for_workspace_ids(
            workspaces_ids,
            start_date=start_date,
            end_date=end_date,
            assignee=assignee,
            custom_task_ids=True,
            token=token,
        )

        task_ids = (
            []
        )  # all unique tasks by ids (one task can appear many times depending on the number of times tracked)
        task_entry_ids = (
            []
        )  # all time tracked ids for all tasks (each time track has its own id)
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
                            if "task" in task.keys()
                            and "custom_id" in task["task"].keys()
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
