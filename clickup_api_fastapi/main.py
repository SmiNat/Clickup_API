from fastapi import FastAPI

from .routers import additional_methods, get_methods

app = FastAPI()

app.include_router(get_methods.router)
app.include_router(additional_methods.router)
