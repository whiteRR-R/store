from typing import Protocol, Optional
from domain.entities.user import User
from application.dtos.user_dto import UserDTO
from application.dtos.login_dto import UserLoginDTO
from application.dtos.reset_password_dto import ResetPasswordDTO


class AuthServiceProtocol(Protocol):
    """ Интерфейс сервиса для управления регистрацией и аутентификацией пользователей. """
    
    async def create_user(self, user_dto: UserDTO) -> None:
        """ Создает нового пользователя, предварительно проверяя существует ли такой пользователь. """
        ...

    async def verify_user_credentials(self, user_credentials: UserLoginDTO) -> User:
        """ Проверяет учетные данные пользователя. """
        ...

    async def _existing_username_or_email(self, username: str, email: str) -> None:
        """ Проверяет, существует ли уже пользователь с таким username или email. """
        ...

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """ Получает пользователя по username или вызывает исключение. """
        ...

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """ Получает пользователя по email или вызывает исключение. """
        ...

    async def update_password(self, username: str, new_password: bytes) -> None:
        """ Обновляет пароль пользователя. """
        ...
