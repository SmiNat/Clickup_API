DATE_SEQUENCE_ERROR = (
    "Type data in a correct sequence (year, month, day[, hour, minute, second])."
)
DATE_TYPE_ERROR = "All components must be integers."
DATE_DATA_ERROR = "Invalid date. Use datetime.datetime() format or enter datetime as a \
    list/tuple with (year, month, day[, hour, minute, second]) values as an integers."
TIME_DURATION_ERROR = "Invalid time duration. Time duration has to be a list/tuple of three elements: \
    days, hours and minutes. To ommit any of those elements, type 0 \
    (eg: [0, 1, 0] for one hour duration)."


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

    def __str__(self) -> str:
        return str(self.message)


class DateValueError(Exception):
    """Exception raised for incorrect date data input."""

    def __init__(self) -> None:
        self.message = DATE_DATA_ERROR

    def __str__(self) -> str:
        return str(self.message)


class TimeDurationError(Exception):
    """Exception raised for incorrect time duration input."""

    def __init__(self) -> None:
        self.message = TIME_DURATION_ERROR

    def __str__(self) -> str:
        return str(self.message)
