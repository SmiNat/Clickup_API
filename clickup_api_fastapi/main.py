import os
from dotenv import load_dotenv
from fastapi import FastAPI
from routers import get_methods, additional_methods


load_dotenv()

app = FastAPI()

app.include_router(get_methods.router)
app.include_router(additional_methods.router)


# TOKEN = os.environ.get("CLICKUP_MY_TOKEN")
TOKEN = os.environ.get("CLICKUP_ADDITIONAL_TOKEN")
URL = os.environ.get("CLICKUP_URL")
HEADER = {"Authorization": TOKEN, "Content-Type": "application/json"}
