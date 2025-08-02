from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka
from presentation.api.v1.router import router as router_v1
from presentation.exception_handlers import register_exception_handlers
from infrastructure.ioc.container import create_container



class Application:
    def __init__(self):
        self.app = FastAPI()
        self.container = create_container()
        self._include_routers()
        setup_dishka(self.container, self.app)
        register_exception_handlers(self.app)

    def _include_routers(self):
        self.app.include_router(router_v1)

        
application = Application()
app = application.app
