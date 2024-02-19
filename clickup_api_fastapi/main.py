from fastapi import FastAPI
from routers import get_methods, additional_methods


app = FastAPI()

app.include_router(get_methods.router)
app.include_router(additional_methods.router)
