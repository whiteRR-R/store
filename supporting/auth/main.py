from fastapi import FastAPI
from container import Container
from domain.exceptions import (
    DomainException,
    ValidationError
)
from application.exceptions import (
    AuthException,
    RegistrationException,
    UserNotFoundException,
    TokenProcessingException,
)
from infrastructure.exceptions import DatabaseException
from exception_handlers import (
    domain_exception_handler,
    validation_exception_handler,
    auth_exception_handler,
    registration_exception_handler,
    user_not_found_exception_handler,
    token_exception_handler,
    database_exception_handler,
    generic_exception_handler,
)

class Application:
    def __init__(self):
        """Инициализирует FastAPI приложение и настраивает зависимости."""
        self.app = FastAPI()
        self.container = Container()
        self._configure_routes()
        self._registration_exception_handler()
        
    def _configure_routes(self):
        """Настраивает маршруты приложения."""
        auth_router = self.container.auth_controller()
        self.app.include_router(router=auth_router.router, tags=["Auth"])
    
    def _registration_exception_handler(self):
        """Обработчик исключений"""
        self.app.add_exception_handler(DomainException, domain_exception_handler)
        self.app.add_exception_handler(ValidationError, validation_exception_handler)
        self.app.add_exception_handler(AuthException, auth_exception_handler)
        self.app.add_exception_handler(RegistrationException, registration_exception_handler)
        self.app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
        self.app.add_exception_handler(TokenProcessingException, token_exception_handler)
        self.app.add_exception_handler(DatabaseException, database_exception_handler)
        self.app.add_exception_handler(Exception, generic_exception_handler)

    def get_app(self) -> FastAPI:
        """Возвращает экземпляр FastAPI."""
        return self.app

application = Application()
app = application.get_app()
