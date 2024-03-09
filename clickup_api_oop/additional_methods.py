from __future__ import annotations

import datetime
from typing import Any

from dotenv import load_dotenv

from .get_methods import ClickUpGETMethods
from .post_put_methods import ClickUpPOSTMethods

load_dotenv()


class ClickUpAdditionalMethods(ClickUpPOSTMethods):

    def request_workspace_ids(
        self, team_id: Any | None = None, token: str | None = None
    ) -> list | tuple:
        """
        If no 'team_id' - returns a list of workspaces (team_ids) authorized for a token
        owner from get_authorized_teams_workspaces request.
        If 'team_id' is provided, verifies if type of data for 'team_id' is correct.

        Args:
            team_id (Any | None, optional): Team ID (Workspace). If None, includes \
                all teams available for token owner. Defaults to None.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            list | tuple: Returns a list or a tuple of team_ids (workspaces).
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
            team_id (list[int] | tuple[int]): Team ID (Workspace).
        Returns:
            list: Returns a list of responses to get_time_entries request.
        """

        if not team_id:
            raise AttributeError("'team_id' must be a list or a tuple with ID values.")

        responses = []
        for team in team_id:
            response = self.get_time_entries(team_id=team, as_json=True, **kwargs)
            if not "data" in response.keys():
                raise ReferenceError(
                    f"Request to access teams failed - team not authorized. "
                    "ClickUp API final error message: {response}."
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
            start_date (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Sets beginning of a time search. If None, equals to the beginning of \
                a current month. Use datetime.datetime() to set a start_date. \
                Alternatively type start_date as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            end_date (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Sets end of a time search. If None, equals to current date and time. \
                Use datetime.datetime() to set a end_date. \
                Alternatively type end_date as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            assignee (int | list[int] | tuple[int] | None, optional): Filter time \
                entries by user_id. Provide the user_id as an integer. For multiple \
                assignees, use a list or a tuple with user_id numbers. \
                Note: Only Workspace Owners/Admins have access to do this.
            team_id (list[int] | tuple[int] | None, optional): Team ID (Workspace). \
                Note: one user may be assigned to more than one team. \
                For receiving worktime from multiple workspaces, type workspace IDs as \
                a list or a tuple. If None, includes all teams available for token owner.
            only_billable (bool, optional): If set to True, calculates time tracked \
                only of tasks with billable set to True. If False, returns all time \
                tracked from time entries request. Defaults to False.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict: Returns a dictionary of usernames with their time tracked from time \
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
            start_date (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Sets beginning of a time search. If None, equals to the beginning of \
                a current month. Use datetime.datetime() to set a start_date.\
                Alternatively type start_date as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            end_date (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Sets end of a time search. If None, equals to current date and time. \
                Use datetime.datetime() to set a end_date. \
                Alternatively type end_date as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            team_id (list[int] | tuple[int] | None, optional): Team ID (Workspace). \
                Note: one user may be assigned to more than one team. \
                To receive tasks from multiple workspaces, type workspace IDs as a list \
                or a tuple. If None, includes all teams available for token owner. \
                Defaults to None.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            dict: Returns a dictionary of a username, a user_id and tasks (task_id, \
                task_name and task total duration) for a selected user (assignee) \
                in a given period of time.
        """

        workspaces_ids = self.request_workspace_ids(team_id=team_id, token=token)

        # for filtering by username and surname instead of user_id:
        workspaces_data = self.get_authorized_teams_workspaces(token=token)
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

        # all unique tasks by ids (one task can appear many times depending on
        # the number of times tracked):
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
                    # increasing time duration for existing task in user_tasks dict
                    # (task with multiple time entrances):
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

    def add_items_to_a_checklist(
        self,
        checklist_id: str,
        items: list[tuple[str, int] | str],
        token: str | None = None,
    ) -> dict:
        """
        Add many items to a single checklist.

        Args:
            checklist_id (str)
            items (list[tuple[str, int]]): List of a checklist items provided as \
                a tuples of (name, assignee_id) pairs. \
                First element of tuple is checklist item name (required), second element \
                of tuple is id of assignee (optional). \
                Alternatively, type a list of strings of item names without any assignees.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns: dict response.
        """

        if isinstance(items, str):
            self.create_checklist_item(
                checklist_id=checklist_id, name=items, token=token
            )
        elif isinstance(items, list):
            for item in items:
                if isinstance(item, tuple):
                    if len(item) == 2:
                        self.create_checklist_item(
                            checklist_id=checklist_id,
                            name=item[0],
                            assignee=item[1],
                            token=token,
                        )
                    else:
                        self.create_checklist_item(
                            checklist_id=checklist_id, name=item, token=token
                        )
                elif isinstance(item, str):
                    self.create_checklist_item(
                        checklist_id=checklist_id, name=item, token=token
                    )
        else:
            raise AttributeError("'items' must be a list or a string.")
        return {"status_code": 201, "detail": "Items added to a checklist."}

    def post_checklist_with_many_items(
        self,
        task_id: str | None = None,
        checklist_id: str | None = None,
        checklist_name: str | None = None,
        checklist_items: list[tuple[str, int] | str] | None = None,
        token: str | None = None,
    ) -> dict:
        """
        Create a new checklist with many items or add multiple items to existing checklist.
        Note: either task_id (for new checklist with items) or checklist_id (for adding
        items to existing checklist) must be set.

        Args:
            task_id (str | None, optional): Required if checklist_id is None. \
                Use to create a new checklist with new items.
            checklist_id (str | None, optional): Required if task_id is None. \
                Use to add new items to existing checklist.
            checklist_name (str | None, optional): Required if task_id is not None.
            checklist_items (list[tuple[str, int]] | None, optional): List of a \
                checklist items provided as a tuples of (name, assignee_id) pairs. \
                First element of tuple is checklist item name (required), second element \
                of tuple is id of assignee (optional). \
                Alternatively, type a list of strings of item names without any assignees.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns: dict response.
        """

        if (not task_id and not checklist_id) or (task_id and checklist_id):
            raise AttributeError(
                "Either 'task_id' or 'checklist_id' must be set (not both)."
            )
        if checklist_name and checklist_id:
            raise AttributeError(
                "Set either 'checklist_name' or 'checklist_id', not both."
            )
        if (task_id and not checklist_name) or (checklist_name and not task_id):
            raise AttributeError(
                "For creating new checklist with items, both team_id' "
                "and 'checklist_name' are required."
            )

        if task_id:
            checklist = self.create_checklist(task_id, checklist_name, token)
            checklist_id = checklist["checklist"]["id"]

        if checklist_items:
            self.add_items_to_a_checklist(checklist_id, checklist_items, token)

        return {"status_code": 201, "detail": "Successfully created."}

    def create_task_with_checklist_and_items(
        self,
        list_id: int,
        task_name: str,
        description: str | None = None,
        parent: str | None = None,
        assignees: list[int] | None = None,
        tags: list[str] | None = None,
        status: str | None = None,
        priority: int | None = None,
        due_date: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        time_estimate: list[int, int, int] | tuple[int, int, int] | None = None,
        start_date: (
            datetime.datetime | list[int, int, int] | tuple[int, int, int] | None
        ) = None,
        notify_all: bool = False,
        links_to: str | None = None,
        checklist_name: str | None = None,
        checklist_items: list[tuple[str, int] | str] | None = None,
        token: str | None = None,
    ) -> dict:
        """
        Post a new task (subtask) with checklist and checklist items.

        Args:
            list_id (int)
            task_name (str)
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
            time_estimate (list[int, int, int] | tuple[int, int, int] | None = None, \
                optional): Estimated time for a task. Use number of days, hours, minutes. \
                Defaults to None.
            start_date (datetime.datetime | list[int] | tuple[int] | None, optional): \
                Use datetime.datetime() to set a start_date. \
                Alternatively type start_date as a list or a tuple of integer values \
                in the following order: (year, month, day[, hour, minute, second]). \
                Defaults to None.
            notify_all (bool): Defaults to False.
            links_to (str | None, optional): Include a task ID to create a linked \
                dependency with your new task.
            checklist_name (str | None, optional): Required if checklist_items is \
                not None. Defaults to None.
            checklist_items (list[tuple[str, int]] | None, optional): List of a \
                checklist items provided as a tuples of (name, assignee_id) pairs. \
                First element of tuple is checklist item name (required), second element \
                of tuple is id of assignee (optional). \
                Alternatively, type a list of strings of item names without any assignees.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns: dict response.
        """

        task = self.create_task(
            list_id=list_id,
            name=task_name,
            description=description,
            parent=parent,
            assignees=assignees,
            tags=tags,
            status=status,
            priority=priority,
            due_date=due_date,
            time_estimate=time_estimate,
            start_date=start_date,
            notify_all=notify_all,
            links_to=links_to,
            token=token,
        )

        if checklist_name:
            checklist = self.create_checklist(
                task_id=task["id"], name=checklist_name, token=token
            )
            checklist_id = checklist["checklist"]["id"]

        if checklist_items:
            if not checklist_name:
                raise AttributeError(
                    "'checklist_name' parameter is required to add " "a checklist item."
                )
            self.add_items_to_a_checklist(checklist_id, checklist_items, token)

        return {
            "status_code": 201,
            "detail": "Task/subtask with checklist was successfully created.",
        }
