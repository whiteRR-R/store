from fastapi import FastAPI
from bootstrap import initializate_auth_controller

app = FastAPI()
auth_controller = initializate_auth_controller()
app.include_router(auth_controller.router, tags=["auth"])