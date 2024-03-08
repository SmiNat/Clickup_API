from fastapi import FastAPI

from .routers import (additional_methods, delete_methods, get_methods,
                      post_put_methods)

app = FastAPI(title="ClickUp API Methods")

app.include_router(additional_methods.router)
app.include_router(get_methods.router)
app.include_router(post_put_methods.router)
app.include_router(delete_methods.router)
