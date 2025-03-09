from fastapi import FastAPI
from container import Container

class Application:
    def __init__(self):
        """Инициализирует FastAPI приложение и настраивает зависимости."""
        self.app = FastAPI()
        self.container = Container()
        self._configure_routes()

    def _configure_routes(self):
        """Настраивает маршруты приложения."""
        auth_router = self.container.auth_controller()
        self.app.include_router(router=auth_router.router, tags=["Auth"])

    def get_app(self) -> FastAPI:
        """Возвращает экземпляр FastAPI."""
        return self.app

application = Application()
app = application.get_app()
