from container import Container
from fastapi import FastAPI
from contextlib import asynccontextmanager


class APP:
    def __init__(self):
        self.container = Container()
        self.app = FastAPI(lifespan=self._lifespan)
        self._initialize_routes()

    def _initialize_routes(self):
        """Initialize routes for the application."""
        category_controller = self.container.category_controller()
        self.app.include_router(router=category_controller.router, tags=["Category"])

    def get_app(self) -> FastAPI:
        """Get the FastAPI application instance."""
        return self.app

    @asynccontextmanager
    async def _lifespan(self, app: FastAPI):
        event_bus = self.container.pub_event_bus()
        await event_bus.connect()
        yield
        await event_bus.close()


Application = APP()
app = Application.get_app()
