DATE_SEQUENCE_ERROR = (
    "Type data in a correct sequence (year, month, day[, hour, minute, second])."
)
DATE_TYPE_ERROR = "All date components must be integers."
DATE_DATA_ERROR = """Invalid date. Use datetime.datetime() format or enter datetime as a
list/tuple with (year, month, day[, hour, minute, second]) values as an integers."""


class DateSequenceError(Exception):
    """Exception raised for incorrect date sequence input."""

    def __init__(self, error: ValueError) -> None:
        self.error = error
        self.message = str(error).capitalize() + ". " + DATE_SEQUENCE_ERROR

    def __str__(self) -> str:
        return str(self.message)


class DateTypeError(Exception):
    """Exception raised for incorrect date type input."""

    def __init__(self, error: TypeError) -> None:
        self.error = error
        self.message = str(error).capitalize() + ". " + DATE_TYPE_ERROR
        self.message = str(error).capitalize() + ". " + DATE_TYPE_ERROR

    def __str__(self) -> str:
        return str(self.message)


class DateValueError(Exception):
    """Exception raised for incorrect date data input."""

    def __init__(self) -> None:
        self.message = DATE_DATA_ERROR

    def __str__(self) -> str:
        return str(self.message)
