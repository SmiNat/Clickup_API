import datetime

import requests

from clickup_api.handlers import (
    check_boolean,
    datetime_to_unix_time_in_milliseconds,
    time_estimate_to_unix_time_in_milliseconds,
)

from .get_methods import ClickUpGETMethods


class ClickUpPOSTMethods(ClickUpGETMethods):

    def create_task(
        self,
        list_id: int,
        name: str,
        custom_task_ids: bool = False,
        team_id: int | None = None,
        description: str | None = None,
        parent: str | None = None,
        assignees: list[int] | None = None,
        tags: list[str] | None = None,
        status: str | None = None,
        priority: int | None = None,
        due_date: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        due_date_time: bool = False,
        time_estimate: list[int, int, int] | tuple[int, int, int] | None = None,
        start_date: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        start_date_time: bool = False,
        notify_all: bool = False,
        links_to: str | None = None,
        check_required_custom_fields: bool = False,
        custom_fields: list[str, str | int] | None = None,
        custom_item_id: int | None = None,
        as_json: bool = True,
        token: str | None = None,
    ):
        """
        Execute POST request - create a new task or a new subtask.
        More info: https://clickup.com/api/clickupreference/operation/CreateTask/

        Args:
            list_id (int)
            name (str): Task name.
            custom_task_ids (bool): If you want to reference a task by it's \
                custom task ID, this value must be set to True. Defaults to False.
            team_id (int | None, optional): Only used when the custom_task_ids \
                parameter is set to True. Defaults to None.
            description (str | None, optional): Task description. Defaults to None.
            parent (str | None, optional): You can create a subtask by including \
                an existing task ID. The parent task ID you include cannot be \
                a subtask, and must be in the same List specified in the path parameter. \
                Defaults to None.
            assignees (list[int] | None, optional): Task Assignees. Defaults to None.
            tags (list[str] | None, optional): Task tags. Defaults to None.
            status (str | None, optional): Task status. Defaults to None.
            priority (int | None, optional): Task priority. Defaults to None.
            due_date (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Use datetime.datetime() to set a due_date. \
                Alternatively type due_date as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            due_date_time (bool): Defaults to False.
            time_estimate (list[int, int, int] | tuple[int, int, int] | None = None, \
                optional): Estimated time for a task. Use number of days, hours, minutes. \
                Defaults to None.
            start_date (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Use datetime.datetime() to set a start_date. \
                Alternatively type start_date as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            start_date_time (bool): Defaults to False.
            notify_all (bool): Defaults to False.
            links_to (str | None, optional): Include a task ID to create a linked \
                dependency with your new task.
            check_required_custom_fields (bool): When creating a task via API \
                any required Custom Fields are ignored by default (False). \
                You can enforce required Custom Fields by including \
                check_required_custom_fields: True.
            custom_fields (list[str, int | str] | None, optional): Array of objects \
                consistent of 'id' (str) and 'value' (int | str).
            custom_item_id (int | None, optional): To create a task that doesn't use \
                a custom task type, either don't include this field in the request \
                body, or send 'null' (None). \
                To create this task as a Milestone, send a value of 1. \
                To use a custom task type, send the custom task type ID as defined \
                in your Workspace, such as 2.
            as_json (bool): If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "list/" + str(list_id) + "/task"

        custom_task_ids = "true" if team_id or custom_task_ids else "false"

        if custom_fields:
            if len(custom_fields) == 2:
                if isinstance(custom_fields[0], str) and isinstance(
                    custom_fields[1], (int, str)
                ):
                    custom_fields = [
                        {"id": str(custom_fields[0]), "value": custom_fields[1]}
                    ]
                else:
                    raise TypeError(
                        "First element of 'custom fields' must be a string. "
                        "Second element must be a string or an integer."
                    )
            else:
                raise ValueError(
                    "'custom fields' must contain two elements: "
                    "id (str) and value (str | int)."
                )

        query = {
            "custom_task_ids": custom_task_ids,
            "team_id": team_id,
        }

        payload = {
            "name": name,
            "description": description,
            "parent": parent,
            "assignees": assignees,
            "tags": tags,
            "status": status,
            "priority": priority,
            "due_date": (
                datetime_to_unix_time_in_milliseconds(due_date)
                if due_date
                else due_date
            ),
            "due_date_time": "true" if check_boolean(due_date_time) else "false",
            "time_estimate": time_estimate_to_unix_time_in_milliseconds(time_estimate),
            "start_date": (
                datetime_to_unix_time_in_milliseconds(start_date)
                if start_date
                else start_date
            ),
            "start_date_time": "true" if check_boolean(start_date_time) else "false",
            "notify_all": "true" if check_boolean(notify_all) else "false",
            "links_to": links_to,
            "check_required_custom_fields": (
                "true" if check_boolean(check_required_custom_fields) else "false"
            ),
            "custom_fields": custom_fields,
            "custom_item_id": custom_item_id,
        }

        response = requests.post(
            url,
            params=query,
            json=payload,
            headers=self.header(token=token, content_type="application/json"),
        )
        return response.json() if as_json else response

    def update_task(
        self,
        task_id: str,
        custom_task_ids: bool = False,
        team_id: int | None = None,
        name: str | None = None,
        description: str | None = None,
        parent: str | None = None,
        assignees_to_remove: list[int] | None = None,
        assignees_to_add: list[int] | None = None,
        status: str | None = None,
        priority: int | None = None,
        due_date: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        due_date_time: bool = False,
        time_estimate: list[int, int, int] | tuple[int, int, int] | None = None,
        start_date: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        start_date_time: bool = False,
        archived: bool = False,
        as_json: bool = True,
        token: str | None = None,
    ):
        """
        Execute PUT request - update a task or a subtask.
        More info: https://clickup.com/api/clickupreference/operation/UpdateTask/
        Note: To update Custom Fields on a task, you must use the Set Custom Field endpoint.

        Args:
            task_id (str)
            custom_task_ids (bool): If you want to reference a task by it's \
                custom task ID, this value must be set to True. Defaults to False.
            team_id (int | None, optional): Only used when the custom_task_ids \
                parameter is set to True. Defaults to None.
            name (str | None, optional): New task name. Defaults to None.
            description (str, optional): New task description. To clear the task \
                description, include Description with " ".
            parent (str | None, optional): You can move a subtask to another parent \
                task by including "parent" with a valid task id. You cannot convert \
                a subtask to a task by setting "parent" to null. Defaults to None.
            assignees_to_remove (list[int] | None, optional): Current task Assignees \
                to remove. Defaults to None.
            assignees_to_add (list[int] | None, optional): New task Assignees to add. \
                Defaults to None.
            status (str | None, optional): Task status. Defaults to None.
            priority (int | None, optional): Task priority. Defaults to None.
            due_date (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Use datetime.datetime() to set a due_date. \
                Alternatively type due_date as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            due_date_time (bool): Defaults to False.
            time_estimate (list[int, int, int] | tuple[int, int, int] | None = None, \
                optional): Estimated time for a task. Use number of days, hours, minutes. \
                Defaults to None.
            start_date (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Use datetime.datetime() to set a start_date. \
                Alternatively type start_date as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            start_date_time (bool): Defaults to False.
            archived (bool): If True, returns response of archived data.
                Defaults to False.
            as_json (bool): If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "task/" + str(task_id)

        custom_task_ids = "true" if team_id or custom_task_ids else "false"

        assignees = {
            "add": [] if assignees_to_add is None else assignees_to_add,
            "rem": [] if assignees_to_remove is None else assignees_to_remove,
        }

        query = {
            "custom_task_ids": custom_task_ids,
            "team_id": team_id,
        }

        payload = {
            "name": name,
            "description": description,
            "status": status,
            "priority": priority,
            "due_date": (
                datetime_to_unix_time_in_milliseconds(due_date)
                if due_date
                else due_date
            ),
            "due_date_time": "true" if check_boolean(due_date_time) else "false",
            "parent": parent,
            "time_estimate": time_estimate_to_unix_time_in_milliseconds(time_estimate),
            "start_date": (
                datetime_to_unix_time_in_milliseconds(start_date)
                if start_date
                else start_date
            ),
            "start_date_time": "true" if check_boolean(start_date_time) else "false",
            "assignees": assignees,
            "archived": "true" if check_boolean(archived) else "false",
        }

        response = requests.put(
            url,
            params=query,
            json=payload,
            headers=self.header(token=token, content_type="application/json"),
        )
        return response.json() if as_json else response

    def create_checklist(
        self,
        task_id: str,
        name: str,
        custom_task_ids: bool = False,
        team_id: int | None = None,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute POST request - add a new checklist to a task.
        More info: https://clickup.com/api/clickupreference/operation/CreateChecklist/

        Args:
            task_id (str)
            name (str): Checklist name.
            custom_task_ids (bool): If you want to reference a task by it's \
                custom task ID, this value must be set to True. Defaults to False.
            team_id (int | None, optional): Only used when the custom_task_ids \
                parameter is set to True. Defaults to None.
            as_json (bool): If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "task/" + str(task_id) + "/checklist"

        custom_task_ids = "true" if team_id or custom_task_ids else "false"

        query = {
            "custom_task_ids": custom_task_ids,
            "team_id": team_id,
        }

        payload = {"name": name}

        response = requests.post(
            url,
            params=query,
            json=payload,
            headers=self.header(token=token, content_type="application/json"),
        )
        return response.json() if as_json else response

    def edit_checklist(
        self,
        checklist_id: str,
        name: str | None = None,
        position: int | None = None,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute PUT request - rename a task checklist, or reorder a checklist so it
        appears above or below other checklists on a task.
        More info: https://clickup.com/api/clickupreference/operation/EditChecklist/

        Args:
            checklist_id (str)
            name (str | None, optional): New checklist name. Defaults to None.
            position (int | None, optional): Position refers to the order of \
                appearance of checklists on a task. To set a checklist to appear \
                at the top of the checklists section of a task, use "position": 0. \
                Defaults to None.
            as_json (bool): If True, returns response as a JSON type. Defaults to None.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "checklist/" + str(checklist_id)

        payload = {"name": name, "position": position}

        response = requests.put(
            url,
            json=payload,
            headers=self.header(token=token, content_type="application/json"),
        )
        return response.json() if as_json else response

    def create_checklist_item(
        self,
        checklist_id: str,
        name: str,
        assignee: int | None = None,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute POST request - add a new checklist to a task.
        More info: https://clickup.com/api/clickupreference/operation/CreateChecklist/

        Args:
            checklist_id (str)
            name (str): Checklist name.
            assignee (int | None, optional): Checklist item Assignee. Defaults to None.
            as_json (bool): If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                    or as a JSON dictionary.
        """

        url = self.api_url + "checklist/" + str(checklist_id) + "/checklist_item"

        payload = {"name": name, "assignee": assignee}

        response = requests.post(
            url,
            json=payload,
            headers=self.header(token=token, content_type="application/json"),
        )
        return response.json() if as_json else response

    def edit_checklist_item(
        self,
        checklist_id: str,
        checklist_item_id: str,
        task_id: str,
        name: str | None = None,
        assignee: int | None = None,
        remove_assignee: bool = False,
        resolved: bool = False,
        parent: str | None = None,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute PUT request - update an individual line item in a task checklist.
        You can rename it, set the assignee, mark it as resolved, or nest it
        under another checklist item.
        More info: https://clickup.com/api/clickupreference/operation/EditChecklistItem/

        Args:
            checklist_id (str)
            checklist_item_id (str)
            task_id (str)
            name (str | None, optional): New checklist item name. Defaults to None.
            assignee (int | None, optional): New checklist item Assignee id. \
                Defaults to None. Note: if None, makes no changes in Assignee id.
            remove_assignee (bool): To remove Assignee from an item and leave it empty. \
                Defaults to False. Note: always False if assignee is not None.
            resolved (bool): Defaults to False.
            parent (str | None, optional): To nest a checklist item under another \
                checklist item, include the other item's checklist_item_id. \
                Defaults to None.
            as_json (bool): If True, returns response as a JSON type. Defaults to None.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = str(
            self.api_url
            + "checklist/"
            + str(checklist_id)
            + "/checklist_item/"
            + str(checklist_item_id)
        )

        remove_assignee = False if assignee else remove_assignee

        if not name or not assignee:
            task = self.get_task(task_id)
            for checklist in task["checklists"]:
                if checklist["id"] == checklist_id:
                    task_checklist = checklist
                    break
            for item in task_checklist["items"]:
                if item["id"] == checklist_item_id:
                    name = item["name"] if not name else name
                    assignee = item["assignee"]["id"] if not assignee else assignee
                    break

        payload = {
            "name": name,
            "assignee": assignee if not remove_assignee else None,
            "resolved": "true" if check_boolean(resolved) else "false",
            "parent": parent,
        }

        response = requests.put(
            url,
            json=payload,
            headers=self.header(token=token, content_type="application/json"),
        )
        return response.json() if as_json else response

    def create_task_comment(
        self,
        task_id: str,
        comment_text: str,
        assignee: int | None = None,
        notify_all: bool = False,
        custom_task_ids: bool = False,
        team_id: int | None = None,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute POST request - add a new comment to a task.
        More info: https://clickup.com/api/clickupreference/operation/CreateTaskComment/

        Args:
            task_id (str)
            comment_text (str)
            assignee (int | None): Defaults to None.
            notify_all (bool): Defaults to False.
            custom_task_ids (bool): If you want to reference a task by it's \
                custom task ID, this value must be set to True. Defaults to False.
            team_id (int | None, optional): Only used when the custom_task_ids \
                parameter is set to True. Defaults to None.
            as_json (bool): If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "task/" + str(task_id) + "/comment"

        custom_task_ids = "true" if team_id or custom_task_ids else "false"

        query = {
            "custom_task_ids": custom_task_ids,
            "team_id": team_id,
        }

        payload = {
            "comment_text": comment_text,
            "assignee": assignee,
            "notify_all": "true" if check_boolean(notify_all) else "false",
        }

        response = requests.post(
            url,
            params=query,
            json=payload,
            headers=self.header(token=token, content_type="application/json"),
        )
        return response.json() if as_json else response

    def create_list_comment(
        self,
        list_id: int,
        comment_text: str,
        assignee: int | None = None,
        notify_all: bool = False,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute POST request - add a comment to a list.
        More info: https://clickup.com/api/clickupreference/operation/CreateListComment/

        Args:
            list_id (int)
            comment_text (str)
            assignee (int | None): Defaults to None.
            notify_all (bool): Defaults to False.
            as_json (bool): If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "list/" + str(list_id) + "/comment"

        payload = {
            "comment_text": comment_text,
            "assignee": assignee,
            "notify_all": "true" if check_boolean(notify_all) else "false",
        }

        response = requests.post(
            url,
            json=payload,
            headers=self.header(token=token, content_type="application/json"),
        )
        return response.json() if as_json else response

    def create_chat_view_comment(
        self,
        view_id: str,
        comment_text: str,
        notify_all: bool = False,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute POST request - add a new comment to a Chat view.
        More info: https://clickup.com/api/clickupreference/operation/CreateChatViewComment/

        Args:
            view_id (str)
            comment_text (str)
            assignee (int | None): Defaults to None.
            as_json (bool): If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "view/" + str(view_id) + "/comment"

        payload = {
            "comment_text": comment_text,
            "notify_all": "true" if check_boolean(notify_all) else "false",
        }

        response = requests.post(
            url,
            json=payload,
            headers=self.header(token=token, content_type="application/json"),
        )
        return response.json() if as_json else response

    def update_comment(
        self,
        comment_id: int,
        comment_text: str,
        assignee: int | str | None = None,
        resolved: bool = False,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute PUT request - replace the content of a task commment, assign a comment,
        and mark a comment as resolved.
        More info: https://clickup.com/api/clickupreference/operation/CreateListComment/

        Args:
            comment_id (int)
            comment_text (str)
            assignee (int | str | None): Use empty string if you wish to delete Assignee \
                form a comment. Defaults to None.
            resolved (bool): Defaults to False.
            as_json (bool): If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "comment/" + str(comment_id)

        payload = {
            "comment_text": comment_text,
            "assignee": assignee,
            "resolved": "true" if check_boolean(resolved) else "false",
        }

        response = requests.put(
            url,
            json=payload,
            headers=self.header(token=token, content_type="application/json"),
        )
        return response.json() if as_json else response

    def add_task_link(
        self,
        task_id: str,
        links_to: str,
        custom_task_ids: bool = False,
        team_id: int | None = None,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute POST request - Link two tasks together.
        More info: https://clickup.com/api/clickupreference/operation/AddTaskLink/

        Args:
            task_id (str)
            links_to (str)
            custom_task_ids (bool): If you want to reference a task by it's \
                custom task ID, this value must be set to True. Defaults to False.
            team_id (int | None, optional): Only used when the custom_task_ids \
                parameter is set to True. Defaults to None.
            as_json (bool): If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "task/" + str(task_id) + "/link/" + str(links_to)

        custom_task_ids = "true" if team_id or custom_task_ids else "false"

        query = {
            "custom_task_ids": custom_task_ids,
            "team_id": team_id,
        }

        response = requests.post(
            url,
            params=query,
            headers=self.header(token=token, content_type="application/json"),
        )
        return response.json() if as_json else response

    def add_task_dependency(
        self,
        task_id: str,
        depends_on: str | None = None,
        dependency_of: str | None = None,
        custom_task_ids: bool = False,
        team_id: int | None = None,
        as_json: bool = True,
        token: str | None = None,
    ) -> dict | requests.Response:
        """
        Execute POST request - Set a task as waiting on or blocking another task.
        More info: https://clickup.com/api/clickupreference/operation/AddDependency/
        Note: either depends_on or dependency_of parameter can be set in request.

        Args:
            task_id (str)
            depends_on (str | None): Use the depends_on parameter in the request body \
                to specify the task that must be completed before the task in the path \
                parameter.
            dependency_of (str | None): Use the dependency_of parameter in the request \
                body to specify the task that's waiting for the task in the path \
                parameter to be completed.
            custom_task_ids (bool): If you want to reference a task by it's \
                custom task ID, this value must be set to True. Defaults to False.
            team_id (int | None, optional): Only used when the custom_task_ids \
                parameter is set to True. Defaults to None.
            as_json (bool): If True, returns response as a JSON type. Defaults to True.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict | Any: Returns response either as a class 'requests.models.Response' \
                or as a JSON dictionary.
        """

        url = self.api_url + "task/" + str(task_id) + "/dependency"

        custom_task_ids = "true" if team_id or custom_task_ids else "false"

        query = {
            "custom_task_ids": custom_task_ids,
            "team_id": team_id,
        }

        if depends_on and dependency_of:
            raise AttributeError(
                "Either 'depends_on' or 'dependency_of' parameter can be set, not both."
            )

        payload = {"depends_on": depends_on, "dependency_of": dependency_of}

        response = requests.post(
            url,
            params=query,
            json=payload,
            headers=self.header(token=token, content_type="application/json"),
        )
        return response.json() if as_json else response
