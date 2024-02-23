import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class Static(str, Enum):
    URL = os.environ.get("CLICKUP_URL")
    # TOKEN = os.environ.get("CLICKUP_ADDITIONAL_TOKEN")
    # TOKEN = os.environ.get("CLICKUP_MAIN_TOKEN")
    TOKEN = os.environ.get("CLICKUP_MY_TOKEN")
