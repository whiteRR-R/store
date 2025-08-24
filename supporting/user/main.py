from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka
from infrastructure.ioc.container import create_container
from presentation.api.v1.router import router as api_v1_router


class Application:
    def __init__(self):
        self.app = FastAPI()
        self.__include_routers()
        self.container = create_container()
        setup_dishka(self.container, self.app)

    def __include_routers(self):
        self.app.include_router(api_v1_router, tags=["auth"])

application = Application()
app = application.app
