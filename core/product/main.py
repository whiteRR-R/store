from contextlib import asynccontextmanager
from fastapi import FastAPI
from container import Container
from presentation.api.endpoints.product import router as product_router
from presentation.api.endpoints.brand import router as brand_router


class Application:
    def __init__(self):
        self.app = FastAPI(lifespan=self._lifespan)
        self.container = Container()
        self._include_routers()

    def _include_routers(self):
        self.app.include_router(product_router, prefix="/api")
        self.app.include_router(brand_router, prefix="/api")

    async def initializate_handlers(self):
        event_bus_subscriber = self.container.event_bus_subscriber()
        category_create_handler = self.container.category_create_handler()
        event_bus_subscriber.register_handler(
            category_create_handler.__class__.__name__,
            category_create_handler.handle
        )

    async def _lifespan(self, app: FastAPI):
        self.container.init_resources()
        event_bus_subscriber = self.container.event_bus_subscriber()
        await event_bus_subscriber.connect()
        await self.initializate_handlers()
        yield
        await event_bus_subscriber.close()


application = Application()
app = application.app
