import datetime
import unittest
from typing import Any
from unittest.mock import patch

from dotenv import load_dotenv
from parameterized import parameterized

from clickup_api.exceptions import DateSequenceError, DateValueError
from clickup_api.handlers import (
    check_and_adjust_list_length,
    check_boolean,
    check_integer_list,
    check_positive_integer,
    check_token,
    date_as_string_to_unix_time_in_milliseconds,
    datetime_to_unix_time_in_milliseconds,
    is_url,
    split_int_array,
    split_string_array,
)

load_dotenv()


class TestHandlers(unittest.TestCase):

    @parameterized.expand(
        [
            ("Valid url", "https://clickup.com/api/", True),
            ("No http", "clickup.com/api/", False),
            ("Empty string as an url", "", False),
        ]
    )
    def test_is_url_validation_is_correct(self, name: str, url: str, result: bool):
        self.assertEqual(is_url(url), result)

    def test_check_token_is_correct(self):
        self.assertIsNone(check_token("some_string"))

    @parameterized.expand(
        [
            ("invalid data type", 123456789, TypeError),
            ("empty string", "", ValueError),
        ]
    )
    def test_check_token_raises_error(self, name: str, value: Any, error: Exception):
        with self.assertRaises(error):
            check_token(value)

    def test_check_positive_integer_success(self):
        self.assertIsNone(check_positive_integer(5))

    @parameterized.expand(
        [
            ("negative integer", -3, ValueError),
            ("float value", 2.33, TypeError),
            ("string value", "3", TypeError),
        ]
    )
    def test_check_positive_integer_raises_error(
        self, name: str, value: Any, error: Exception
    ):
        with self.assertRaises(error):
            check_positive_integer(value)

    def test_check_integer_list_success(self):
        self.assertIsNone(check_integer_list([3, 6, -9]))
        self.assertIsNone(check_integer_list([]))

    @parameterized.expand(
        [
            ("tuple instead of a list", (1, 2, 3), TypeError),
            ("string instead of a list", "1, 2, 3", TypeError),
            ("list with float numbers", [1, 2, 3.33], TypeError),
            ("list with string values", [1, 2, "3"], TypeError),
        ]
    )
    def test_check_integer_list_raises_error(
        self, name: str, value: Any, error: Exception
    ):
        with self.assertRaises(error):
            check_integer_list(value)

    def test_check_boolean_success(self):
        self.assertTrue(check_boolean(True))
        self.assertFalse(check_boolean(False))

    @parameterized.expand(
        [
            ("tuple instead of a boolean", (1, 2), TypeError),
            ("string instead of a boolean", "1, 3", TypeError),
            ("list instead of a boolean", [1, 2], TypeError),
            ("integer instead of a boolean", 11, TypeError),
            ("floating number instead of a boolean", 1.21, TypeError),
        ]
    )
    def test_check_boolean_raises_error(self, name: str, value: Any, error: Exception):
        with self.assertRaises(error):
            check_boolean(value)

    @parameterized.expand(
        [
            (
                "test datetime.datetime format",
                datetime.datetime(2024, 11, 22, 8, 55),
                1732262100000.0,
            ),
            ("test list format", [2024, 10, 10], 1728511200000.0),
            ("test tuple format", (2024, 7, 7, 7, 55), 1720331700000.0),
        ]
    )
    def test_datetime_to_unix_time_in_milliseconds_success(
        self, name: str, value: Any, expected: int | float
    ):
        self.assertEqual(datetime_to_unix_time_in_milliseconds(value), expected)

    @parameterized.expand(
        [
            ("incorrect list format", [10, 10, 2024], DateSequenceError),
            ("incorrect tuple format", (7, 7, 2024), DateSequenceError),
            ("incorrect data type", "2024, 11, 11", DateValueError),
        ]
    )
    def test_datetime_to_unix_time_in_milliseconds_raises_error(
        self, name: str, value: Any, error: Exception
    ):
        with self.assertRaises(error):
            self.assertEqual(datetime_to_unix_time_in_milliseconds(value))

    @parameterized.expand(
        [
            ("test list format", "2024, 10, 10", 1728511200000.0),
            ("test tuple format", "2024, 7, 7, 7, 55", 1720331700000.0),
        ]
    )
    def test_date_as_string_to_unix_time_in_milliseconds_success(
        self, name: str, value: Any, expected: int | float
    ):
        self.assertEqual(date_as_string_to_unix_time_in_milliseconds(value), expected)

    @parameterized.expand(
        [
            (
                "correct type with incorrect date value",
                "2024, 110, 10",
                DateSequenceError,
            ),
            ("incorrect data type", ["2024, 7, 7, 7, 55"], TypeError),
        ]
    )
    def test_date_as_string_to_unix_time_in_milliseconds_raises_error(
        self, name: str, value: Any, error: Exception
    ):
        with self.assertRaises(error):
            self.assertEqual(date_as_string_to_unix_time_in_milliseconds(value))

    @parameterized.expand(
        [
            ("empty list", False, [], []),
            ("single element list with an integer", True, [1], [1, 1234]),
            ("single element list with a string", False, ["3Def5"], ["3Def5", "Abc1"]),
            ("multiple element list with integers", True, [1, -2, 3], [1, -2, 3]),
            ("multiple element list with strings", False, ["3D", "xyz"], ["3D", "xyz"]),
        ]
    )
    @patch("random.choices")
    def test_check_and_adjust_list_length_success(
        self,
        name: str,
        append_number: bool,
        value: list,
        expected: list,
        mocked_choices,
    ):
        if append_number:
            mocked_choices.return_value = ["1", "2", "3", "4"]
        elif not append_number:
            mocked_choices.return_value = ["A", "b", "c", "1"]
        self.assertEqual(check_and_adjust_list_length(value, append_number), expected)

    @parameterized.expand(
        [
            ("tuple instead of a list", True, (1, 2), TypeError),
            ("string instead of a list", False, "1, 3", TypeError),
            ("integer instead of a list", True, 11, TypeError),
            ("floating number instead of a list", True, 1.21, TypeError),
        ]
    )
    def test_check_and_adjust_list_length_raises_error(
        self, name: str, append_number: bool, value: list, error: Exception
    ):
        with self.assertRaises(error):
            check_and_adjust_list_length(value, append_number)


if __name__ == "__main__":
    unittest.main(verbosity=1)
