import datetime
import os
import unittest
from typing import Any
from unittest.mock import patch

import requests
from dotenv import load_dotenv
from parameterized import parameterized

from ..get_methods import ClickUpGETMethods

load_dotenv()

# python -m unittest clickup_api_oop.tests.test_clickup_api_get_methods. --f


class TestClickUpGETAuthorizedTeamsWorkspacesRequests(unittest.TestCase):
    """Tests for get_authorized_teams_workspaces method of ClickUpGETMethods class."""

    @classmethod
    def setUpClass(cls):
        cls.token = os.environ.get("CLICKUP_MY_TOKEN")
        cls.instance = ClickUpGETMethods(cls.token)

    def test_get_authorized_teams_workspaces_returns_200(self):
        response = self.instance.get_authorized_teams_workspaces(as_json=False)
        self.assertEqual(response.status_code, 200)

    def test_get_authorized_teams_workspaces_invalid_token_returns_401(self):
        response = self.instance.get_authorized_teams_workspaces(
            as_json=False, token="TokenRandomCode123"
        )
        self.assertEqual(response.status_code, 401)

    def test_get_authorized_teams_workspaces_returns_json_dict(self):
        response = self.instance.get_authorized_teams_workspaces(as_json=True)
        self.assertIsInstance(response, dict)

    def test_get_authorized_teams_workspaces_returns_response_object(self):
        response = self.instance.get_authorized_teams_workspaces(as_json=False)
        self.assertIsInstance(response, requests.models.Response)


class TestClickUpGETTeamsRequests(unittest.TestCase):
    """Tests for get_teams method of ClickUpGETMethods class."""

    @classmethod
    def setUpClass(cls):
        cls.token = os.environ.get("CLICKUP_MY_TOKEN")
        cls.superior_token = os.environ.get("CLICKUP_MAIN_TOKEN")
        cls.user = os.environ.get("CLICKUP_USER_ID")
        cls.team = os.environ.get("CLICKUP_TEAM_ID_AKADEMIA_MQS")

        cls.instance = ClickUpGETMethods(cls.token)

    def test_get_teams_plain_returns_200(self):
        # Note: won't work with token of too low credentials (status code 400).
        response = self.instance.get_teams(as_json=False, token=self.superior_token)
        self.assertEqual(response.status_code, 200)

    def test_get_teams_with_team_id_returns_200(self):
        response = self.instance.get_teams(self.team, as_json=False)
        self.assertEqual(response.status_code, 200)

    def test_get_teams_with_invalid_team_id_returns_401(self):
        response = self.instance.get_teams(12345678, as_json=False)
        self.assertEqual(response.status_code, 401)

    def test_get_teams_with_invalid_team_id_returns_500(self):
        response = self.instance.get_teams("invalid10", as_json=False)
        self.assertEqual(response.status_code, 500)

    def test_get_teams_invalid_token_returns_401(self):
        invalid_token_instance = ClickUpGETMethods("TokenRandomCode123")
        response = invalid_token_instance.get_teams(self.team, as_json=False)
        self.assertEqual(response.status_code, 401)

    def test_get_teams_returns_json_dict(self):
        response = self.instance.get_teams(self.team, as_json=True)
        self.assertIsInstance(response, dict)

    def test_get_teams_returns_response_object(self):
        response = self.instance.get_teams(self.team, as_json=False)
        self.assertIsInstance(response, requests.models.Response)


class TestClickUpGETSpacesRequests(unittest.TestCase):
    """Tests for get_spaces method of ClickUpGETMethods class."""

    @classmethod
    def setUpClass(cls):
        cls.token = os.environ.get("CLICKUP_MY_TOKEN")
        cls.instance = ClickUpGETMethods(cls.token)
        cls.team = os.environ.get("CLICKUP_TEAM_ID_AKADEMIA_MQS")

    def test_get_spaces_with_required_team_id_returns_200(self):
        response = self.instance.get_spaces(team_id=self.team, as_json=False)
        self.assertEqual(response.status_code, 200)

    def test_get_spaces_without_team_id_returns_500(self):
        response = self.instance.get_spaces(team_id=None, as_json=False)
        self.assertEqual(response.status_code, 500)

    def test_get_spaces_with_invalid_team_id_returns_500(self):
        response = self.instance.get_spaces(team_id="invalid10", as_json=False)
        self.assertEqual(response.status_code, 500)

    def test_get_spaces_with_invalid_team_id_returns_401(self):
        response = self.instance.get_spaces(team_id=123456789, as_json=False)
        self.assertEqual(response.status_code, 401)

    def test_get_spaces_invalid_token_returns_401(self):
        response = self.instance.get_spaces(
            team_id=self.team, as_json=False, token="TokenRandomCode123"
        )
        self.assertEqual(response.status_code, 401)

    def test_get_spaces_returns_json_dict(self):
        response = self.instance.get_spaces(team_id=self.team, as_json=True)
        self.assertIsInstance(response, dict)

    def test_get_spaces_returns_response_object(self):
        response = self.instance.get_spaces(team_id=self.team, as_json=False)
        self.assertIsInstance(response, requests.models.Response)


class TestClickUpGETFoldersRequests(unittest.TestCase):
    """Tests for get_folders method of ClickUpGETMethods class."""

    @classmethod
    def setUpClass(cls):
        cls.token = os.environ.get("CLICKUP_MY_TOKEN")
        cls.instance = ClickUpGETMethods(cls.token)
        cls.space = os.environ.get("CLICKUP_SPACE_ID_MQUBE")

    def test_get_folders_with_required_space_id_returns_200(self):
        response = self.instance.get_folders(space_id=self.space, as_json=False)
        self.assertEqual(response.status_code, 200)

    def test_get_folders_without_space_id_returns_400(self):
        response = self.instance.get_folders(space_id=None, as_json=False)
        self.assertEqual(response.status_code, 400)

    def test_get_folders_with_invalid_space_id_returns_400(self):
        response = self.instance.get_folders(space_id="invalid10", as_json=False)
        self.assertEqual(response.status_code, 400)

    def test_get_folders_with_invalid_space_id_returns_401(self):
        response = self.instance.get_folders(space_id=123456789, as_json=False)
        self.assertEqual(response.status_code, 401)

    def test_get_folders_invalid_token_returns_401(self):
        response = self.instance.get_folders(
            space_id=self.space, as_json=False, token="TokenRandomCode123"
        )
        self.assertEqual(response.status_code, 401)

    def test_get_folders_returns_json_dict(self):
        response = self.instance.get_folders(space_id=self.space, as_json=True)
        self.assertIsInstance(response, dict)

    def test_get_folders_returns_response_object(self):
        response = self.instance.get_folders(space_id=self.space, as_json=False)
        self.assertIsInstance(response, requests.models.Response)

    def test_get_folders_with_archived_returns_200(self):
        response = self.instance.get_folders(
            space_id=self.space, archived=True, as_json=False
        )
        self.assertEqual(response.status_code, 200)


class TestClickUpGETListsRequests(unittest.TestCase):
    """Tests for get_lists method of ClickUpGETMethods class."""

    @classmethod
    def setUpClass(cls):
        cls.token = os.environ.get("CLICKUP_MY_TOKEN")
        cls.instance = ClickUpGETMethods(cls.token)
        cls.folder = os.environ.get("CLICKUP_FOLDER_ID_SPRINT_FOLDER_IN_SPACE_MQUBE")

    def test_get_lists_with_required_folder_id_returns_200(self):
        response = self.instance.get_lists(folder_id=self.folder, as_json=False)
        self.assertEqual(response.status_code, 200)

    def test_get_lists_without_folder_id_returns_400(self):
        response = self.instance.get_lists(folder_id=None, as_json=False)
        self.assertEqual(response.status_code, 400)

    def test_get_lists_with_invalid_folder_id_returns_400(self):
        response = self.instance.get_lists(folder_id="invalid10", as_json=False)
        self.assertEqual(response.status_code, 400)

    def test_get_lists_with_invalid_folder_id_returns_401(self):
        response = self.instance.get_lists(folder_id=123456789, as_json=False)
        self.assertEqual(response.status_code, 401)

    def test_get_lists_invalid_token_returns_401(self):
        response = self.instance.get_lists(
            folder_id=self.folder, as_json=False, token="TokenRandomCode123"
        )
        self.assertEqual(response.status_code, 401)

    def test_get_lists_returns_json_dict(self):
        response = self.instance.get_lists(folder_id=self.folder, as_json=True)
        self.assertIsInstance(response, dict)

    def test_get_lists_returns_response_object(self):
        response = self.instance.get_lists(folder_id=self.folder, as_json=False)
        self.assertIsInstance(response, requests.models.Response)

    def test_get_lists_with_archived_returns_200(self):
        response = self.instance.get_lists(
            folder_id=self.folder, archived=True, as_json=False
        )
        self.assertEqual(response.status_code, 200)


class TestClickUpGETTasksRequests(unittest.TestCase):
    """Tests for get_task method of ClickUpGETMethods class."""

    @classmethod
    def setUpClass(cls):
        cls.token = os.environ.get("CLICKUP_MY_TOKEN")
        cls.user = os.environ.get("CLICKUP_USER_ID")
        cls.team = os.environ.get("CLICKUP_TEAM_ID_AKADEMIA_MQS")

        cls.list = os.environ.get("CLICKUP_LIST_ID_LIST_IN_FOLDER_TEST_IN_MQUBE")
        cls.task_with_subtasks = os.environ.get(
            "CLICKUP_TASK_ID_ZW_IN_LIST_IN_FOLDER_TEST_IN_MQUBE"
        )
        cls.subtask = os.environ.get(
            "CLICKUP_SUBTASK_ID_ZP_TO_ZW_IN_LIST_IN_FOLDER_TEST_IN_MQUBE"
        )

        cls.instance = ClickUpGETMethods(cls.token)

    def test_get_tasks_with_required_list_id_returns_200(self):
        response = self.instance.get_tasks(self.list, as_json=False)
        self.assertEqual(response.status_code, 200)

    def test_get_tasks_invalid_token_returns_401(self):
        invalid_token_instance = ClickUpGETMethods("TokenRandomCode123")
        response = invalid_token_instance.get_tasks(self.list, as_json=False)
        self.assertEqual(response.status_code, 401)

    def test_get_tasks_without_list_id_returns_401(self):
        response = self.instance.get_tasks(list_id=None, as_json=False)
        self.assertEqual(response.status_code, 401)

    def test_get_tasks_with_invalid_list_id_returns_400(self):
        response = self.instance.get_tasks(list_id="invalid10", as_json=False)
        self.assertEqual(response.status_code, 400)

    def test_get_tasks_with_invalid_list_id_returns_401(self):
        response = self.instance.get_tasks(list_id=12345678, as_json=False)
        self.assertEqual(response.status_code, 401)

    def test_get_tasks_returns_json_dict(self):
        response = self.instance.get_tasks(self.list, as_json=True)
        self.assertIsInstance(response, dict)

    def test_get_tasks_returns_response_object(self):
        response = self.instance.get_tasks(self.list, as_json=False)
        self.assertIsInstance(response, requests.models.Response)

    def test_get_tasks_archived_returns_200(self):
        response = self.instance.get_tasks(self.list, archived=True, as_json=False)
        self.assertEqual(response.status_code, 200)

    def test_get_tasks_with_markdown_description_returns_200(self):
        response = self.instance.get_tasks(
            self.list, include_markdown_description=True, as_json=False
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("markdown_description", response.content.decode())

    def test_get_tasks_with_page_number_returns_200(self):
        response = self.instance.get_tasks(self.list, page=1, as_json=False)
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(
        [
            ("correct type: id", "id"),
            ("correct type: created", "created"),
            ("correct type: updated", "updated"),
            ("correct type: due_date", "due_date"),
        ]
    )
    def test_get_tasks_with_order_by_returns_200(self, name: str, value: str):
        response = self.instance.get_tasks(self.list, order_by=value, as_json=False)
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(
        [
            ("incorrect type: int", 123, TypeError),
            ("correct type: list", ["created", "id"], TypeError),
            ("correct string", "incorrect", ValueError),
        ]
    )
    def test_get_tasks_with_inorrect_order_by_returns_error(
        self, name: str, value: str, error: Exception
    ):
        # ClickUp API response: 500 "Internal server error"
        with self.assertRaises(error):
            self.instance.get_tasks(self.list, order_by=value, as_json=False)

    def test_get_tasks_reverse_returns_200(self):
        response = self.instance.get_tasks(self.list, reverse=True, as_json=False)
        self.assertEqual(response.status_code, 200)

    def test_get_tasks_with_subtasks_returns_200(self):
        response = self.instance.get_tasks(self.list, subtasks=True, as_json=False)
        self.assertEqual(response.status_code, 200)
        print(response.json())
        self.assertIn(self.subtask, response.content.decode())

    @parameterized.expand(
        [
            ("correct type: empty list", []),
            ("correct type: list with one element", ["created"]),
            ("correct type: list of any data", [123, True, "zamknięte"]),
        ]
    )
    def test_get_tasks_by_statuses_returns_200(self, name: str, value: str):
        response = self.instance.get_tasks(self.list, statuses=value, as_json=False)
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(
        [
            ("incorrect type: int", 123, TypeError),
            ("correct type: tuple", ("nowe", "gotowe"), TypeError),
            ("incorrect type: string", "nowe", TypeError),
        ]
    )
    def test_get_tasks_with_inorrect_statuses_returns_error(
        self, name: str, value: str, error: Exception
    ):
        # ClickUp API response: 500 "Internal server error"
        with self.assertRaises(error):
            self.instance.get_tasks(self.list, statuses=value, as_json=False)

    def test_get_tasks_include_closed_returns_200(self):
        response = self.instance.get_tasks(
            self.list, include_closed=True, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(
        [
            ("empty list", []),
            ("single element list", ["nowe"]),
            ("multiple fake elements in a list", ["xyz", "abc", "123"]),
        ]
    )
    def test_get_tasks_with_assignees_returns_200(self, name: str, value: list):
        response = self.instance.get_tasks(self.list, assignees=value, as_json=False)
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(
        [
            ("empty list", []),
            ("single element list", ["nowe"]),
            ("multiple fake elements in a list", ["xyz", "abc", "123"]),
        ]
    )
    def test_get_tasks_with_tags_returns_200(self, name: str, value: list):
        response = self.instance.get_tasks(self.list, tags=value, as_json=False)
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(
        [
            ("empty list", []),
            ("single element list", [123]),
            ("multiple fake elements in a list", [123, 456, 789]),
        ]
    )
    def test_get_tasks_with_custom_items_returns_200(self, name: str, value: list):
        response = self.instance.get_tasks(self.list, custom_items=value, as_json=False)
        self.assertEqual(response.status_code, 200)

    def test_get_tasks_with_custom_fields_returns_error(self):
        with self.assertRaises(NotImplementedError):
            self.instance.get_tasks(self.list, custom_fields=True, as_json=False)

    @parameterized.expand(
        [
            ("datetime field", datetime.datetime(2024, 1, 10)),
            ("tuple field", (2024, 1, 10)),
            ("list field", [2024, 1, 10]),
        ]
    )
    def test_get_tasks_with_date_fields_200(self, name: str, value: Any):
        response = self.instance.get_tasks(
            self.list,
            due_date_gt=value,
            due_date_lt=value,
            date_created_gt=value,
            date_created_lt=value,
            date_updated_gt=value,
            date_updated_lt=value,
            date_done_gt=value,
            date_done_lt=value,
            as_json=False,
        )
        self.assertEqual(response.status_code, 200)


class TestClickUpGETTaskRequests(unittest.TestCase):
    """Tests for get_task method of ClickUpGETMethods class."""

    @classmethod
    def setUpClass(cls):
        cls.token = os.environ.get("CLICKUP_MY_TOKEN")
        cls.user = os.environ.get("CLICKUP_USER_ID")
        cls.team = os.environ.get("CLICKUP_TEAM_ID_AKADEMIA_MQS")

        cls.task_with_subtasks = os.environ.get(
            "CLICKUP_TASK_ID_ZW_IN_LIST_IN_FOLDER_TEST_IN_MQUBE"
        )
        cls.subtask = os.environ.get(
            "CLICKUP_SUBTASK_ID_ZP_TO_ZW_IN_LIST_IN_FOLDER_TEST_IN_MQUBE"
        )

        cls.instance = ClickUpGETMethods(cls.token)

    def test_get_task_with_required_task_id_returns_200(self):
        response = self.instance.get_task(self.task_with_subtasks, as_json=False)
        self.assertEqual(response.status_code, 200)

    def test_get_task_invalid_token_returns_401(self):
        invalid_token_instance = ClickUpGETMethods("TokenRandomCode123")
        response = invalid_token_instance.get_task(
            self.task_with_subtasks, as_json=False
        )
        self.assertEqual(response.status_code, 401)

    def test_get_task_without_task_id_returns_401(self):
        response = self.instance.get_task(task_id=None, as_json=False)
        self.assertEqual(response.status_code, 401)

    def test_get_task_with_invalid_task_id_returns_401(self):
        """Invalid task_id value."""
        response = self.instance.get_task("invalid10", as_json=False)
        self.assertEqual(response.status_code, 401)

    def test_get_task_with_invalid_task_id_returns_401(self):
        """Invalid data type for task_id (integer instead of a string)."""
        response = self.instance.get_task(12345678, as_json=False)
        self.assertEqual(response.status_code, 401)

    def test_get_task_returns_json_dict(self):
        response = self.instance.get_task(self.task_with_subtasks, as_json=True)
        self.assertIsInstance(response, dict)

    def test_get_task_returns_response_object(self):
        response = self.instance.get_task(self.task_with_subtasks, as_json=False)
        self.assertIsInstance(response, requests.models.Response)

    def test_get_task_with_markdown_description_returns_200(self):
        response = self.instance.get_task(
            self.task_with_subtasks, include_markdown_description=True, as_json=False
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("markdown_description", response.content.decode())

    def test_get_task_with_subtasks_returns_200(self):
        response = self.instance.get_task(
            self.task_with_subtasks, include_subtasks=True, as_json=False
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["subtasks"])
        self.assertIn(self.subtask, response.content.decode())

    def test_get_task_with_team_id_returns_200(self):
        response = self.instance.get_task(
            self.task_with_subtasks, team_id=self.team, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    def test_get_task_with_incorrect_team_id_returns_401(self):
        # 401 if team_id is an invalid number
        response = self.instance.get_task(
            self.task_with_subtasks, team_id=123456789, as_json=False
        )
        self.assertEqual(response.status_code, 401)

    def test_get_task_with_incorrect_team_id_returns_500(self):
        # 500 if team_id is a string (invalid data type)
        response = self.instance.get_task(
            self.task_with_subtasks, team_id="invalid10", as_json=False
        )
        self.assertEqual(response.status_code, 500)


class TestClickUpGETUserRequests(unittest.TestCase):
    """
    Tests for get_user method of ClickUpGETMethods class.
    Note: This endpoint is only available to Workspaces on Enterprise Plan.
    """

    @classmethod
    def setUpClass(cls):
        cls.token = os.environ.get("CLICKUP_MY_TOKEN")
        cls.superior_token = os.environ.get("CLICKUP_MAIN_TOKEN")
        cls.user = os.environ.get("CLICKUP_USER_ID")
        cls.team = os.environ.get("CLICKUP_TEAM_ID_AKADEMIA_MQS")

        cls.instance = ClickUpGETMethods(cls.token)

    # Test without Entreprise Plan on ClickUp
    def test_get_user_returns_403_without_enterprise_plan(self):
        response = self.instance.get_user(
            team_id=self.team,
            user_id=self.user,
            as_json=False,
            token=self.superior_token,
        )
        self.assertEqual(response.status_code, 403)

    # Test with Entreprise Plan on ClickUp -  not implemented


class TestClickUpGETTimeEntriesRequests(unittest.TestCase):
    """Tests for get_time_entries method of ClickUpGETMethods class."""

    @classmethod
    def setUpClass(cls):
        cls.superior_token = os.environ.get("CLICKUP_MAIN_TOKEN")
        cls.token = os.environ.get("CLICKUP_MY_TOKEN")
        cls.user = os.environ.get("CLICKUP_USER_ID")
        cls.team = os.environ.get("CLICKUP_TEAM_ID_AKADEMIA_MQS")

        cls.space = os.environ.get("CLICKUP_SPACE_ID_MQUBE")
        cls.folder = os.environ.get("CLICKUP_FOLDER_ID_SPRINT_FOLDER_IN_SPACE_MQUBE")
        cls.list = os.environ.get("CLICKUP_LIST_ID_LIST_IN_FOLDER_TEST_IN_MQUBE")
        cls.task_with_subtasks = os.environ.get(
            "CLICKUP_TASK_ID_ZW_IN_LIST_IN_FOLDER_TEST_IN_MQUBE"
        )

        cls.user2 = os.environ.get("CLICKUP_USER_ID_VLADYSLAV")
        cls.user3 = os.environ.get("CLICKUP_USER_ID_MICHAL")

        cls.instance = ClickUpGETMethods(cls.token)

    def test_get_time_entries_minimal_request_with_team_id_returns_200(self):
        response = self.instance.get_time_entries(self.team, as_json=False)
        self.assertEqual(response.status_code, 200)

    def test_get_time_entries_minimal_request_without_team_id_returns_500(self):
        response = self.instance.get_time_entries(team_id=None, as_json=False)
        self.assertEqual(response.status_code, 500)

    def test_get_time_entries_minimal_request_with_invalid_team_id_returns_401(self):
        """Invalid team_id value."""
        response = self.instance.get_time_entries(team_id=123456789, as_json=False)
        self.assertEqual(response.status_code, 401)

    def test_get_time_entries_minimal_request_with_invalid_team_id_returns_500(self):
        """Invalid data type for team_id (string instead of a integer)"""
        response = self.instance.get_time_entries(team_id="invalid10", as_json=False)
        self.assertEqual(response.status_code, 500)

    def test_get_time_entries_invalid_token_returns_401(self):
        invalid_token_instance = ClickUpGETMethods("TokenRandomCode123")
        response = invalid_token_instance.get_time_entries(self.team, as_json=False)
        self.assertEqual(response.status_code, 401)

    def test_get_time_entries_minimal_request_returns_json_dict(self):
        response = self.instance.get_time_entries(self.team, as_json=True)
        self.assertIsInstance(response, dict)

    def test_get_time_entries_minimal_request_returns_response_object(self):
        response = self.instance.get_time_entries(self.team, as_json=False)
        self.assertIsInstance(response, requests.models.Response)

    @parameterized.expand(
        [
            ("start date as datetime.datetime", datetime.datetime(2023, 11, 20)),
            ("start date as a list", [2023, 11, 20]),
            ("start date as a tuple", (2023, 11, 20)),
        ]
    )
    def test_get_time_entries_with_start_date_200(self, name: str, value: Any):
        response = self.instance.get_time_entries(
            self.team, start_date=value, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(
        [
            ("end date as datetime.datetime", datetime.datetime(2024, 1, 10)),
            ("end date as a list", [2024, 1, 10]),
            ("end date as a tuple", (2024, 1, 10)),
        ]
    )
    def test_get_time_entries_with_end_date_200(self, name: str, value: Any):
        response = self.instance.get_time_entries(
            self.team, end_date=value, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(
        [
            ("datetime and a list", datetime.datetime(2024, 1, 10), [2024, 2, 10]),
            ("tuple and datetime", (2024, 1, 10), datetime.datetime(2024, 2, 10)),
        ]
    )
    def test_get_time_entries_with_start_date_and_end_date_200(
        self, name: str, start: Any, end: Any
    ):
        response = self.instance.get_time_entries(
            self.team, start_date=start, end_date=end, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    def test_get_time_entries_with_assignee_200(self):
        # Note: With too low token credentials returns 403
        cases = [
            ("one assignee", self.user2),
            ("two assignees as a list", [self.user2, self.user3]),
            ("two assignees as a tuple", (self.user2, self.user3)),
        ]
        for name, value in cases:
            with self.subTest(cases=cases):
                response = self.instance.get_time_entries(
                    self.team, assignee=value, as_json=False, token=self.superior_token
                )
                self.assertEqual(response.status_code, 200)

    def test_get_time_entries_with_include_task_tags_returns_200(self):
        response = self.instance.get_time_entries(
            self.team, include_location_names=True, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    def test_get_time_entries_with_include_location_names_returns_200(self):
        response = self.instance.get_time_entries(
            self.team, include_location_names=True, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    def test_get_time_entries_with_custom_task_ids_returns_200(self):
        response = self.instance.get_time_entries(
            self.team, custom_task_ids=True, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    def test_get_time_entries_with_space_id_returns_200(self):
        response = self.instance.get_time_entries(
            self.team, space_id=self.space, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    def test_get_time_entries_with_folder_id_returns_200(self):
        response = self.instance.get_time_entries(
            self.team, folder_id=self.folder, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    def test_get_time_entries_with_list_id_returns_200(self):
        response = self.instance.get_time_entries(
            self.team, list_id=self.list, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    def test_get_time_entries_with_task_id_returns_200(self):
        response = self.instance.get_time_entries(
            self.team, task_id=self.task_with_subtasks, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    def test_get_time_entries_with_space_id_and_folder_id_returns_400(self):
        # Note: Only one of the following location filters can be included at a time:
        # space_id, folder_id, list_id, or task_id.
        response = self.instance.get_time_entries(
            self.team, space_id=self.space, folder_id=self.folder, as_json=False
        )
        self.assertEqual(response.status_code, 400)

    def test_get_time_entries_with_query_team_id_returns_200(self):
        # Test with random team_id number as no teams are set in ClickUp (team != workspace)
        response = self.instance.get_time_entries(
            self.team, query_team_id=123456789, as_json=False
        )
        self.assertEqual(response.status_code, 200)


class TestClickUpGETAuthorizedUserRequests(unittest.TestCase):
    """Tests for get_authorized_user method of ClickUpGETMethods class."""

    @classmethod
    def setUpClass(cls):
        cls.token = os.environ.get("CLICKUP_MY_TOKEN")
        cls.instance = ClickUpGETMethods(cls.token)

    def test_get_authorized_user_returns_200(self):
        response = self.instance.get_authorized_user(as_json=False)
        self.assertEqual(response.status_code, 200)

    def test_get_authorized_user_invalid_token_returns_401(self):
        response = self.instance.get_authorized_user(
            as_json=False, token="TokenRandomCode123"
        )
        self.assertEqual(response.status_code, 401)

    def test_get_authorized_user_returns_json_dict(self):
        response = self.instance.get_authorized_user(as_json=True)
        self.assertIsInstance(response, dict)

    def test_get_authorized_user_returns_response_object(self):
        response = self.instance.get_authorized_user(as_json=False)
        self.assertIsInstance(response, requests.models.Response)


class TestClickUpGETTaskCommentsRequests(unittest.TestCase):
    """Tests for get_task_comments method of ClickUpGETMethods class."""

    @classmethod
    def setUpClass(cls):
        cls.token = os.environ.get("CLICKUP_MY_TOKEN")
        cls.user = os.environ.get("CLICKUP_USER_ID")
        cls.team = os.environ.get("CLICKUP_TEAM_ID_AKADEMIA_MQS")

        cls.task = os.environ.get(
            "CLICKUP_TASK_ID_UCP_IN_SPRINT1_IN_SPRINT_FOLDER_IN_MQUBE"
        )
        cls.comment = os.environ.get("CLICKUP_COMMENT_TASK_ID")

        cls.instance = ClickUpGETMethods(cls.token)

    def test_get_task_comments_with_required_task_id_returns_200(self):
        response = self.instance.get_task_comments(task_id=self.task, as_json=False)
        self.assertEqual(response.status_code, 200)

    def test_get_task_comments_invalid_token_returns_401(self):
        invalid_token_instance = ClickUpGETMethods("TokenRandomCode123")
        response = invalid_token_instance.get_task_comments(
            task_id=self.task, as_json=False
        )
        self.assertEqual(response.status_code, 401)

    @parameterized.expand(
        [
            ("no task_id", None),
            ("invalid task_id value", "invalid10"),
            (
                "i6 5wqnvalid data type for task_id (integer instead of a string).",
                123456789,
            ),
        ]
    )
    def test_get_task_comments_without_task_id_returns_401(self, name: str, value: Any):
        response = self.instance.get_task_comments(task_id=value, as_json=False)
        self.assertEqual(response.status_code, 401)

    def test_get_task_comments_returns_json_dict(self):
        response = self.instance.get_task_comments(self.task, as_json=True)
        self.assertIsInstance(response, dict)

    def test_get_task_comments_returns_response_object(self):
        response = self.instance.get_task_comments(self.task, as_json=False)
        self.assertIsInstance(response, requests.models.Response)

    def test_get_task_comments_with_custom_task_ids_returns_200(self):
        response = self.instance.get_task_comments(
            task_id=self.task, custom_task_ids=True, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    def test_get_task_comments_with_team_id_returns_200(self):
        response = self.instance.get_task_comments(
            task_id=self.task, team_id=self.team, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    def test_get_task_comments_with_incorrect_team_id_returns_401(self):
        # 401 if team_id is an invalid number
        response = self.instance.get_task_comments(
            task_id=self.task, team_id=123456789, as_json=False
        )
        self.assertEqual(response.status_code, 401)

    def test_get_task_comments_with_incorrect_team_id_returns_500(self):
        # 500 if team_id is a string (invalid data type)
        response = self.instance.get_task_comments(
            self.task, team_id="invalid10", as_json=False
        )
        self.assertEqual(response.status_code, 500)

    def test_get_task_comments_with_start_id_returns_200(self):
        response = self.instance.get_task_comments(
            self.task, start_id=self.comment, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(
        [
            ("start date as datetime.datetime", datetime.datetime(2023, 11, 20)),
            ("start date as a list", [2023, 11, 20]),
            ("start date as a tuple", (2023, 11, 20)),
        ]
    )
    def test_get_task_comments_with_start_returns_200(self, name: str, value: Any):
        response = self.instance.get_task_comments(
            self.task, start=value, as_json=False
        )
        self.assertEqual(response.status_code, 200)


class TestClickUpGETListCommentsRequests(unittest.TestCase):
    """Tests for get_list_comments method of ClickUpGETMethods class."""

    @classmethod
    def setUpClass(cls):
        cls.token = os.environ.get("CLICKUP_MY_TOKEN")
        cls.user = os.environ.get("CLICKUP_USER_ID")
        cls.team = os.environ.get("CLICKUP_TEAM_ID_AKADEMIA_MQS")

        cls.list = os.environ.get("CLICKUP_LIST_ID_LIST_IN_FOLDER_TEST_IN_MQUBE")
        cls.comment = os.environ.get("CLICKUP_COMMENT_LIST_ID")

        cls.instance = ClickUpGETMethods(cls.token)

    def test_get_list_comments_with_required_list_id_returns_200(self):
        response = self.instance.get_list_comments(list_id=self.list, as_json=False)
        self.assertEqual(response.status_code, 200)

    def test_get_list_comments_invalid_token_returns_401(self):
        invalid_token_instance = ClickUpGETMethods("TokenRandomCode123")
        response = invalid_token_instance.get_list_comments(
            list_id=self.list, as_json=False
        )
        self.assertEqual(response.status_code, 401)

    def test_get_list_comments_with_invalid_list_id_returns_401(self):
        response = self.instance.get_list_comments(list_id=123456789, as_json=False)
        self.assertEqual(response.status_code, 401)

    @parameterized.expand(
        [
            ("no task_id", None),
            ("invalid task_id value", "invalid10"),
        ]
    )
    def test_get_list_comments_incorrect_list_id_returns_400(
        self, name: str, value: Any
    ):
        response = self.instance.get_list_comments(list_id=value, as_json=False)
        self.assertEqual(response.status_code, 400)

    def test_get_list_comments_returns_json_dict(self):
        response = self.instance.get_list_comments(self.list, as_json=True)
        self.assertIsInstance(response, dict)

    def test_get_list_comments_returns_response_object(self):
        response = self.instance.get_list_comments(self.list, as_json=False)
        self.assertIsInstance(response, requests.models.Response)

    def test_get_list_comments_with_start_id_returns_200(self):
        response = self.instance.get_list_comments(
            list_id=self.list, start_id=self.comment, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(
        [
            ("start date as datetime.datetime", datetime.datetime(2023, 11, 20)),
            ("start date as a list", [2023, 11, 20]),
            ("start date as a tuple", (2023, 11, 20)),
        ]
    )
    def test_get_list_comments_with_start_returns_200(self, name: str, value: Any):
        response = self.instance.get_list_comments(
            list_id=self.list, start=value, as_json=False
        )
        self.assertEqual(response.status_code, 200)


'''
class TestClickUpGETChatViewCommentsRequests(unittest.TestCase):
    """Tests for get_chat_view_comments method of ClickUpGETMethods class."""

    @classmethod
    def setUpClass(cls):
        cls.token = os.environ.get("CLICKUP_MY_TOKEN")
        cls.user = os.environ.get("CLICKUP_USER_ID")
        cls.team = os.environ.get("CLICKUP_TEAM_ID_AKADEMIA_MQS")

        cls.view = None     # not available for verification
        cls.comment = None  # not available for verification

        cls.instance = ClickUpGETMethods(cls.token)

    def test_get_chat_view_comments_with_required_view_id_returns_200(self):
        response = self.instance.get_chat_view_comments(
            view_id=self.view, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    def test_get_chat_view_comments_invalid_token_returns_401(self):
        invalid_token_instance = ClickUpGETMethods("TokenRandomCode123")
        response = invalid_token_instance.get_chat_view_comments(
            view_id=self.view, as_json=False
        )
        self.assertEqual(response.status_code, 401)

    def test_get_chat_view_comments_with_invalid_view_id_returns_401(self):
        response = self.instance.get_chat_view_comments(view_id=123456789, as_json=False)
        self.assertEqual(response.status_code, 401)

    @parameterized.expand(
        [
            ("no task_id", None),
            ("invalid task_id value", "invalid10"),
        ]
    )
    def test_get_chat_view_comments_incorrect_view_id_returns_400(
        self, name: str, value: Any):
        response = self.instance.get_chat_view_comments(view_id=value, as_json=False)
        self.assertEqual(response.status_code, 400)

    def test_get_chat_view_comments_returns_json_dict(self):
        response = self.instance.get_chat_view_comments(view_id=self.view, as_json=True)
        self.assertIsInstance(response, dict)

    def test_get_chat_view_comments_returns_response_object(self):
        response = self.instance.get_chat_view_comments(view_id=self.view, as_json=False)
        self.assertIsInstance(response, requests.models.Response)

    def test_get_chat_view_comments_with_start_id_returns_200(self):
        response = self.instance.get_chat_view_comments(
            view_id=self.view, start_id=self.comment, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(
        [
            ("start date as datetime.datetime", datetime.datetime(2023, 11, 20)),
            ("start date as a list", [2023, 11, 20]),
            ("start date as a tuple", (2023, 11, 20)),
        ]
    )
    def test_get_chat_view_comments_with_start_returns_200(self, name: str, value: Any):
        response = self.instance.get_chat_view_comments(
            view_id=self.view, start=value, as_json=False
        )
        self.assertEqual(response.status_code, 200)
'''


class TestClickUpGETCustomTaskTypesRequests(unittest.TestCase):
    """Tests for get_custom_task_types method of ClickUpGETMethods class."""

    @classmethod
    def setUpClass(cls):
        cls.token = os.environ.get("CLICKUP_MY_TOKEN")
        cls.instance = ClickUpGETMethods(cls.token)
        cls.team = os.environ.get("CLICKUP_TEAM_ID_AKADEMIA_MQS")

    def test_get_custom_task_types_with_required_team_id_returns_200(self):
        response = self.instance.get_custom_task_types(team_id=self.team, as_json=False)
        self.assertEqual(response.status_code, 200)

    def test_get_custom_task_types_without_team_id_returns_500(self):
        response = self.instance.get_custom_task_types(team_id=None, as_json=False)
        self.assertEqual(response.status_code, 500)

    def test_get_custom_task_types_with_invalid_team_id_returns_500(self):
        response = self.instance.get_custom_task_types(
            team_id="invalid10", as_json=False
        )
        self.assertEqual(response.status_code, 500)

    def test_get_custom_task_types_with_invalid_team_id_returns_401(self):
        response = self.instance.get_custom_task_types(team_id=123456789, as_json=False)
        self.assertEqual(response.status_code, 401)

    def test_get_custom_task_types_invalid_token_returns_401(self):
        response = self.instance.get_custom_task_types(
            team_id=self.team, as_json=False, token="TokenRandomCode123"
        )
        self.assertEqual(response.status_code, 401)

    def test_get_custom_task_types_returns_json_dict(self):
        response = self.instance.get_custom_task_types(team_id=self.team, as_json=True)
        self.assertIsInstance(response, dict)

    def test_get_custom_task_types_returns_response_object(self):
        response = self.instance.get_custom_task_types(team_id=self.team, as_json=False)
        self.assertIsInstance(response, requests.models.Response)


class TestClickUpGETAccesibleCustomFieldsRequests(unittest.TestCase):
    """Tests for get_accessible_custom_fields method of ClickUpGETMethods class."""

    @classmethod
    def setUpClass(cls):
        cls.token = os.environ.get("CLICKUP_MY_TOKEN")
        cls.instance = ClickUpGETMethods(cls.token)
        cls.list = os.environ.get("CLICKUP_LIST_ID_LIST_IN_FOLDER_TEST_IN_MQUBE")

    def test_get_accessible_custom_fields_with_required_list_id_returns_200(self):
        response = self.instance.get_accessible_custom_fields(
            list_id=self.list, as_json=False
        )
        self.assertEqual(response.status_code, 200)

    def test_get_accessible_custom_fields_without_list_id_returns_400(self):
        response = self.instance.get_accessible_custom_fields(
            list_id=None, as_json=False
        )
        self.assertEqual(response.status_code, 400)

    def test_get_accessible_custom_fields_with_invalid_list_id_returns_400(self):
        response = self.instance.get_accessible_custom_fields(
            list_id="invalid10", as_json=False
        )
        self.assertEqual(response.status_code, 400)

    def test_get_accessible_custom_fields_with_invalid_list_id_returns_401(self):
        response = self.instance.get_accessible_custom_fields(
            list_id=123456789, as_json=False
        )
        self.assertEqual(response.status_code, 401)

    def test_get_accessible_custom_fields_invalid_token_returns_401(self):
        response = self.instance.get_accessible_custom_fields(
            list_id=self.list, as_json=False, token="TokenRandomCode123"
        )
        self.assertEqual(response.status_code, 401)

    def test_get_accessible_custom_fields_returns_json_dict(self):
        response = self.instance.get_accessible_custom_fields(
            list_id=self.list, as_json=True
        )
        self.assertIsInstance(response, dict)

    def test_get_accessible_custom_fields_returns_response_object(self):
        response = self.instance.get_accessible_custom_fields(
            list_id=self.list, as_json=False
        )
        self.assertIsInstance(response, requests.models.Response)


if __name__ == "__main__":
    unittest.main(verbosity=1)
