from dotenv import load_dotenv

from clickup_api.handlers import check_token, is_url

from .enums import ClickupActions

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

    @property
    def token(self) -> str:
        """Returns token."""
        return str(self._token)

    @token.setter
    def token(self, new_token: str) -> None:
        """Sets a new token."""
        check_token(new_token)
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
        elif not is_url(url):
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
            check_token(token)
            api_key = str(token)
        request_header = {"Authorization": api_key, "Content-Type": content_type}
        return request_header
