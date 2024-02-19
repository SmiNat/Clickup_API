import unittest
from typing import Any
from unittest.mock import patch

from dotenv import load_dotenv
from parameterized import parameterized

from ..main import ClickUpAPI

load_dotenv()

# python -m unittest clickup_api_oop.tests.test_clickup_api --f


class TestClickUpAPICore(unittest.TestCase):

    def test_initiate_class_instance_successful(self):
        token = "TokenRandomCode123"
        sample = ClickUpAPI(token)
        self.assertTrue(sample.__dict__)
        self.assertIsInstance(sample, ClickUpAPI)

    def test_empty_token_at_instance_initiation_raises_error(self):
        with self.assertRaises(TypeError):
            ClickUpAPI()

    @parameterized.expand(
        [
            ("Token as a boolean type", True, TypeError),
            ("Token as a list", ["value"], TypeError),
            ("Token as a None value", None, TypeError),
            ("Token as an empty string", "", ValueError),
            ("Token as a dict", {"token": "ABCD1234"}, TypeError),
        ]
    )
    def test_invalid_token_at_instance_initiation_raises_error(
        self, name: str, token: Any, error: Exception
    ):
        with self.assertRaises(error):
            ClickUpAPI(token)

    @parameterized.expand(
        [
            ("Token as an empty string", "", ValueError),
            ("Invalid type of token - float", 123456.99, TypeError),
            ("Invalid type of token - None", None, TypeError),
            ("Invalid type of token - boolean", True, TypeError),
        ]
    )
    def test_token_setter_method_validation_is_correct(
        self, name: str, token: Any, error: Exception
    ):
        initial_token = "TokenRandomCode123"
        sample = ClickUpAPI(initial_token)
        with self.assertRaises(error):
            sample.token = token

    def test_available_statuses_initial_list(self):
        available_statuses = [
            "nowe",
            "w trakcie",
            "oczekujące",
            "odrzucone",
            "gotowe",
            "zamknięte",
        ]
        self.assertEqual(ClickUpAPI.available_statuses, available_statuses)

    def test_class_constant_api_default_url_correct_value(self):
        api_default_url = "https://app.clickup.com/api/v2/"
        self.assertEqual(ClickUpAPI._API_DEFAULT_URL, api_default_url)

    def test_default_url_initial_value(self):
        sample = ClickUpAPI("token")
        expected_url = "https://app.clickup.com/api/v2/"
        self.assertEqual(sample.api_url, expected_url)

    @parameterized.expand(
        [
            ("No http", "clickup.com/api/", ValueError),
            ("Empty string as an url", "", ValueError),
            ("Invalid type of url address - int", 123456, TypeError),
        ]
    )
    def test_invalid_api_url_at_instance_initiation_raises_error(
        self, name: str, url: str, error: Exception
    ):
        token = "TokenRandomCode123"
        with self.assertRaises(error):
            ClickUpAPI(token, url)

    @parameterized.expand(
        [
            ("No http", "clickup.com/api/", ValueError),
            ("Empty string as an url", "", ValueError),
            ("Invalid type of url address - int", 123456, TypeError),
        ]
    )
    def test_api_url_setter_method_validation_is_correct_raises_error(
        self, name: str, url: str, error: Exception
    ):
        token = "TokenRandomCode123"
        sample = ClickUpAPI(token)
        with self.assertRaises(error):
            sample.api_url = url

    def test_api_url_setter_method_endswith_slash(self):
        token = "TokenRandomCode123"
        url = "https://clickup.com/api"
        sample = ClickUpAPI(token, url)
        self.assertTrue(str(sample.api_url).endswith("/"))

    def test_header_method_sets_correct_token(self):
        token = "TokenRandomCode123"
        sample = ClickUpAPI(token)
        self.assertEqual(sample.__dict__["_token"], token)
        self.assertEqual(sample.header()["Authorization"], token)
        header_token = "ABCD1234"
        self.assertEqual(
            sample.header(token=header_token)["Authorization"], header_token
        )
        self.assertEqual(sample.__dict__["_token"], token)

    def test_header_method_sets_correct_content_type(self):
        token = "TokenRandomCode123"
        sample = ClickUpAPI(token)
        build_in_content_type = sample.header()["Content-Type"]
        new_content_type = "text/html"
        self.assertEqual(
            sample.header(content_type=new_content_type)["Content-Type"],
            new_content_type,
        )
        self.assertNotEqual(
            sample.header(content_type=new_content_type)["Content-Type"],
            build_in_content_type,
        )

    @parameterized.expand(
        [
            ("adding new status", "do rozważenia", "add", 1),
            ("adding existing status", "nowe", "add", 0),
            ("removing existing status", "nowe", "remove", -1),
            ("removing non-existing status", "random123string", "remove", 0),
        ]
    )
    def test_available_statuses_list_update_success(
        self, name: str, new_status: str, action: str, change: int
    ):
        number_of_statuses = len(ClickUpAPI.available_statuses)
        ClickUpAPI.change_available_status(new_status, action)
        self.assertEqual(
            len(ClickUpAPI.available_statuses), number_of_statuses + change
        )
        if action == "add":
            self.assertIn(new_status, ClickUpAPI.available_statuses)
        elif action == "remove":
            self.assertNotIn(new_status, ClickUpAPI.available_statuses)

    @parameterized.expand(
        [
            ("adding new status with incorrect action", "do rozważenia", "incorrect"),
            ("removing existing status with incorrect action", "nowe", "incorrect"),
        ]
    )
    def test_available_statuses_list_update_raises_error(
        self, name: str, new_status: str, action: str
    ):
        with self.assertRaises(ValueError):
            ClickUpAPI.change_available_status(new_status, action)


if __name__ == "__main__":
    unittest.main(verbosity=1)
