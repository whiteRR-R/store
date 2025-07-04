from typing import Protocol
from application.dtos.user_dto import UserDTO
from application.dtos.change_email import ChangeEmailDTO
from application.dtos.login_dto import UserLoginDTO
from application.dtos.jwt_token_dto import JWTTokenDTO, JWTTokensDTO
from application.dtos.forgot_password_dto import ForgotPasswordDTO
from application.dtos.reset_password_dto import ResetPasswordDTO


class AuthUseCaseProtocol(Protocol):
    async def register(self, user_data: UserDTO) -> None:
        """
        Регистрация нового пользователя. Проверяет, существует ли уже пользователь с таким именем, 
        и если нет, создает нового пользователя.
        """
        ...

    async def login(self, user_credentials: UserLoginDTO) -> JWTTokensDTO:
        """ Аутентифицирует пользователя и возвращает JWT токены. """
        ...
        
    async def logout(self, access_token: str, refresh_token: str) -> None:
        """ Выход пользователя"""
        ...

    async def delete(self, jwt_token: str) -> None:
        """ Удаляет пользователя по access-токену. """
        ...

    async def get_current_user_info(self, jwt_token: str) -> UserDTO:
        """ Возвращает информацию текущего пользователя. """
        ...

    async def generate_access_token_from_refresh(self, jwt_token: str) -> str:
        """ Генерирует новый access-токен на основе валидного refresh-токена. """
        ...

    async def forgot_password(self, forgot_dto: ForgotPasswordDTO) -> str:
        """ Генерирует reset-токен для сброса пароля. """
        ...

    async def reset_password(self, reset_dto: ResetPasswordDTO) -> None:
        """ Сбрасывает пароль через reset-токен. """
        ...
    
    async def update_email(self, token: str, change_email_dto: ChangeEmailDTO) -> None:
        """ Обновляет email пользователя. """
        ...
