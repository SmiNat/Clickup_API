import datetime
import random
import string
from urllib.parse import urlparse

from .exceptions import DateSequenceError, DateTypeError, DateValueError


def is_url(url: str) -> bool:
    """Validates url address."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def check_token(token: str) -> None:
    """Validates token."""
    if not isinstance(token, str):
        raise TypeError(f"Token must be of type: str, not {type(token)}.")
    if isinstance(token, str) and len(token) == 0:
        raise ValueError("Empty string is not allowed.")


def check_positive_integer(value: int) -> None:
    """Validates if argument is a positive integer."""
    if not isinstance(value, int):
        raise TypeError(f"'{value}' must be an integer, not {type(value)} type.")
    if isinstance(value, int) and value < 0:
        raise ValueError("Only positive number is allowed.")


def check_integer_list(data: list[int]) -> None:
    """Validates if data is a list of integers."""
    if not isinstance(data, list):
        raise TypeError(f"'{data}' must be a list, not {type(data)} type.")
    for element in data:
        if not isinstance(element, int):
            raise TypeError("All list items must be integers.")


def check_boolean(value: bool) -> bool:
    """Validates if value is a boolean."""
    if not isinstance(value, bool):
        raise TypeError(f"'{value}' must be of type: boolean, not {type(value)}.")
    return value


def datetime_to_unix_time_in_milliseconds(
    date: datetime.datetime | list[int] | tuple[int],
) -> int:
    """Converts datetime.date or date represented by the list of [year, month, day] or
    a tuple of (year, month day) to unix time in milliseconds."""
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
            raise DateValueError()
    return date


def date_as_string_to_unix_time_in_milliseconds(date: str) -> int:
    """Converts date expressed as a string of numbers separeted by commas to a list
    of integers and then converts it to unix time in milliseconds."""
    if date:
        if isinstance(date, str):
            split_data = [str(_).strip() for _ in date.split(",")]
            string_to_int = [int(_) for _ in split_data]
            # print("🖥️ ", datetime_to_unix_time_in_milliseconds(string_to_int))
            return datetime_to_unix_time_in_milliseconds(string_to_int)
    return date


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


def split_string_array(data: list[str]) -> list:
    """Converts one-element list to a list of strings."""
    if data:
        if not isinstance(data, list):
            raise TypeError("Invalid data type. Only 'list' of strings is allowed.")
        if len(data) > 1:
            return data  # lists with more than one element are not validated
        split_data = [str(_).strip() for _ in data[0].split(",")]
        if len(split_data) == 1:
            random_value = "".join(
                random.choices(string.ascii_letters + string.digits, k=8)
            )
            split_data.append(random_value)
        return split_data
    return data


def split_int_array(data: list[str]) -> list:
    """Converts one-element list with string to a list of integers."""
    if data:  # empty list is not validated
        if not isinstance(data, list):
            raise TypeError(
                "Invalid data type. Only 'list' with a single string element containing numbers is allowed."
            )
        if len(data) != 1:
            raise ValueError(
                "The list must contain a single string element with numbers separated by commas."
            )
        if isinstance(data[0], str):
            try:
                data = [int(str(_).strip()) for _ in data[0].strip(",").split(",")]
            except ValueError:
                raise ValueError(
                    "The list must contain a single string with numbers separated by commas."
                )
        if (
            len(data) == 1
            and isinstance(data[0], int)
            and not isinstance(data[0], bool)
        ):
            random_value = int("".join(random.choices(string.digits, k=8)))
            data.append(random_value)
        return data  # single-element lists with element other than integer are not validated
    return data
