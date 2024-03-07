import requests

from .main import ClickUpAPI


class ClickUpDELETEMethods(ClickUpAPI):

    def delete_comment(
        self,
        comment_id: int,
        token: str | None = None,
    ) -> tuple[dict | int]:
        """
        Execute DELETE request - delete a comment.
        More info: https://clickup.com/api/clickupreference/operation/DeleteComment/

        Args:
            comment_id (str)
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns:
            tuple [dict | int]: Returns response JSON and status code.
        """

        url = self.api_url + "comment/" + str(comment_id)

        response = requests.delete(url, headers=self.header(token=token))
        return response.json(), response

    def remove_task_from_a_list(
        self,
        list_id: int,
        task_id: str,
        token: str | None = None,
    ) -> int:
        """
        Execute DELETE request - remove a task from an additional List.
        You can't remove a task from its home List.
        Note: This endpoint requires the Tasks in Multiple List ClickApp to be enabled.
        More info: https://clickup.com/api/clickupreference/operation/RemoveTaskFromList/

        Args:
            list_id (int)
            task_id (str)
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns: response status code.
        """

        url = self.api_url + "list/" + str(list_id) + "/task/" + str(task_id)

        response = requests.delete(url, headers=self.header(token=token))
        return response.json(), response.status_code

    def delete_task(
        self,
        task_id: str,
        custom_task_ids: bool = False,
        team_id: int | None = None,
        token: str | None = None,
    ) -> int:
        """
        Execute DELETE request - delete a task from your Workspace.
        More info: https://clickup.com/api/clickupreference/operation/DeleteTask/

        Args:
            task_id (str)
            custom_task_ids (bool): If you want to reference a task by it's \
                custom task ID, this value must be set to True. Defaults to False.
            team_id (int | None, optional): Only used when the custom_task_ids \
                parameter is set to True. Defaults to None.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns: response status code.
        """

        url = self.api_url + "task/" + str(task_id)

        custom_task_ids = "true" if team_id or custom_task_ids else "false"

        query = {
            "custom_task_ids": custom_task_ids,
            "team_id": team_id,
        }

        response = requests.delete(
            url,
            params=query,
            headers=self.header(token=token, content_type="application/json"),
        )
        return response.status_code

    def delete_checklist(self, checklist_id: str, token: str | None = None) -> int:
        """
        Execute DELETE request - delete a checklist from a task.
        More info: https://clickup.com/api/clickupreference/operation/DeleteChecklist/

        Args:
            checklist_id (str)
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns: response status code.
        """
        url = self.api_url + "checklist/" + str(checklist_id)

        response = requests.delete(url, headers=self.header(token=token))
        return response.status_code

    def delete_checklist_item(
        self, checklist_id: str, checklist_item_id: str, token: str | None = None
    ) -> int:
        """
        Execute DELETE request - delete a line item from a task checklist.
        More info: https://clickup.com/api/clickupreference/operation/DeleteChecklistItem/

        Args:
            checklist_id (str)
            checklist_item_id (str)
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns: response status code.
        """
        url = (
            self.api_url
            + "checklist/"
            + str(checklist_id)
            + "/checklist_item/"
            + str(checklist_item_id)
        )

        response = requests.delete(
            url, headers=self.header(token=token, content_type="appliaction/json")
        )
        return response.status_code

    def delete_task_link(
        self,
        task_id: str,
        links_to: str,
        custom_task_ids: bool = False,
        team_id: int | None = None,
        token: str | None = None,
    ) -> int:
        """
        Execute DELETE request - remove the link between two tasks.
        More info: https://clickup.com/api/clickupreference/operation/DeleteTaskLink/

        Args:
            task_id (str)
            links_to (str)
            custom_task_ids (bool): If you want to reference a task by it's \
                custom task ID, this value must be set to True. Defaults to False.
            team_id (int | None, optional): Only used when the custom_task_ids \
                parameter is set to True. Defaults to None.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns: response status code.
        """
        url = self.api_url + "task/" + str(task_id) + "/link/" + str(links_to)

        custom_task_ids = "true" if team_id or custom_task_ids else "false"

        query = {"custom_task_ids": custom_task_ids, "team_id": team_id}

        response = requests.delete(
            url,
            params=query,
            headers=self.header(token=token, content_type="appliaction/json"),
        )
        return response.status_code

    def delete_dependency(
        self,
        task_id: str,
        depends_on: str | None = None,
        dependency_of: str | None = None,
        custom_task_ids: bool = False,
        team_id: int | None = None,
        token: str | None = None,
    ) -> int:
        """
        Execute DELETE request - remove the dependency relationship between two or more tasks.
        More info: https://clickup.com/api/clickupreference/operation/DeleteDependency/

        Args:
            task_id (str)
            depends_on (str, optional)
            dependency_of (str, optional)
            custom_task_ids (bool): If you want to reference a task by it's \
                custom task ID, this value must be set to True. Defaults to False.
            team_id (int | None, optional): Only used when the custom_task_ids \
                parameter is set to True. Defaults to None.
            token (str | None, optional): Token for request authentication. \
                If None, uses token of an instance. Defaults to None.
        Returns: response status code.
        """
        url = self.api_url + "task/" + str(task_id) + "/dependency"

        custom_task_ids = "true" if team_id or custom_task_ids else "false"

        query = {
            "depends_on": depends_on,
            "dependency_of": dependency_of,
            "custom_task_ids": custom_task_ids,
            "team_id": team_id,
        }

        response = requests.delete(
            url,
            params=query,
            headers=self.header(token=token, content_type="appliaction/json"),
        )
        return response.status_code
