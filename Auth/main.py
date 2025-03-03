from fastapi import FastAPI
from container import Container

app = FastAPI()
container = Container()
auth_router = container.auth_controller()
app.include_router(router=auth_router.router, tags=["Auth"])
