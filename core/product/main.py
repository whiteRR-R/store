from fastapi import FastAPI
from container import Container
from domain.exceptions import InvalidValueException, NotFoundException, AlreadyExistException
from application.exceptions import DataNotFoundException
from infrastructure.exceptions import RollbackException
from presentation.api.endpoints.product import router as product_router
from presentation.api.endpoints.brand import router as brand_router
from presentation.api.endpoints.category import router as category_router
from exception_handlers import (
    data_not_found_exception_handler,
    rollback_exception_handler,
    invalid_value_exception_handler,
    not_found_exception_handler,
    already_exist_exception_handler,
)


class Application:
    def __init__(self):
        self.app = FastAPI(lifespan=self._lifespan)
        self.container = Container()
        self._include_routers()

    def _include_routers(self):
        self.app.include_router(product_router, prefix="/api")
        self.app.include_router(brand_router, prefix="/api")
        self.app.include_router(category_router, prefix="/api")
    
    def _registration_exception_handlers(self):
        self.app.add_exception_handler(DataNotFoundException, data_not_found_exception_handler)
        self.app.add_exception_handler(RollbackException, rollback_exception_handler)
        self.app.add_exception_handler(InvalidValueException, invalid_value_exception_handler)
        self.app.add_exception_handler(NotFoundException, not_found_exception_handler)
        self.app.add_exception_handler(AlreadyExistException, already_exist_exception_handler)

    async def _initializate_handlers(self):
        event_bus_subscriber = self.container.event_bus_subscriber()
        category_create_handler = self.container.category_create_handler()
        event_bus_subscriber.register_handler(
            category_create_handler.__class__.__name__,
            category_create_handler.handle
        )

    async def _lifespan(self, app: FastAPI):
        s3 = self.container.s3_storage()
        await s3.ensure_bucket()
        event_bus_subscriber = self.container.event_bus_subscriber()
        await event_bus_subscriber.connect()
        await self.initializate_handlers()
        yield
        await event_bus_subscriber.close()


application = Application()
app = application.app
