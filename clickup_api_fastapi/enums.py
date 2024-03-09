import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class Static(str, Enum):
    URL = "https://app.clickup.com/api/v2"
    TOKEN = os.environ.get("CLICKUP_MY_TOKEN")
