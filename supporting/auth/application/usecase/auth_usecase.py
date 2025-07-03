from domain.interface.services.auth_service import AuthServiceProtocol
from domain.interface.services.jwt_service import JWTServiceProtocol
from application.dtos.user_dto import UserDTO
from application.dtos.login_dto import UserLoginDTO
from application.dtos.jwt_token_dto import JWTTokenDTO
from application.dtos.forgot_password_dto import ForgotPasswordDTO
from application.dtos.reset_password_dto import ResetPasswordDTO
from application.exceptions import (
    InvalidCredentialsException,
    UserNotFoundException,
    UsernameAlreadyExistsException,
    EmailAlreadyExistsException,
    TokenProcessingException,
)
from config import config_manager


class AuthUseCase:
    def __init__(
        self,
        auth_service: AuthServiceProtocol,
        jwt_service: JWTServiceProtocol,
    ):
        self.auth_service = auth_service
        self.jwt_service = jwt_service
    
    async def register(self, user_data: UserDTO):
        """
        Регистрация нового пользователя. Проверяет, существует ли уже пользователь с таким именем, 
        и если нет, создает нового пользователя.
        """
        try:
            await self.auth_service.create_user(user_data)
        except UsernameAlreadyExistsException:
            raise UsernameAlreadyExistsException(user_data.username)
        except EmailAlreadyExistsException:
            raise EmailAlreadyExistsException(user_data.email)
    
    async def login(self, user_credentials: UserLoginDTO):
        """
        Логин пользователя. Проверяет правильность имени пользователя и пароля, затем создает токены.
        """
        try: 
            await self.auth_service.verify_user_credentials(user_credentials)
            return self.jwt_service.generate_jwt_tokens(user_credentials.username)
        except UserNotFoundException:
            raise InvalidCredentialsException()
        except InvalidCredentialsException:
            raise InvalidCredentialsException()
            
    async def forgot_password(self, forgot_dto: ForgotPasswordDTO):
        """ Генерирует reset-токен для сброса пароля """
        try:
            user = await self.auth_service.get_user_by_email(forgot_dto.email)
            if not user:
                raise UserNotFoundException(f"User with email '{forgot_dto.email}' not found.")
            reset_token = self.jwt_service.create_reset_token({"sub": user.username})
            # TODO: Добавить отправку ссылки для сброса на почту
            return reset_token
        except UserNotFoundException:
            raise UserNotFoundException(f"User with email '{forgot_dto.email}' not found.")
        except Exception as e:
            raise TokenProcessingException(f"Failed to generate reset token: {str(e)}")
    
    async def reset_password(self, reset_dto: ResetPasswordDTO):
        """ Сбрасывает пароль через reset-токен """
        try:
            self.jwt_service.validate_token_type(
                jwt_token=reset_dto.reset_token, 
                token_type=config_manager.jwt.RESET_TOKEN_TYPE
            )
            username = self.jwt_service.get_token_subject(reset_dto.reset_token)
            await self.auth_service.update_password(username, reset_dto.new_password.encode())  
        except UserNotFoundException:
            raise UserNotFoundException(f"User '{username}' not found for password reset.")
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Invalid reset token: {str(e)}")
    
    async def get_current_user_info(self, jwt_token: str):
        """ Возвращает информацию о текущем пользователе """
        try:
            self.jwt_service.validate_token_type(
                jwt_token=jwt_token, 
                token_type=config_manager.jwt.ACCESS_TOKEN_TYPE
            )
            subject = self.jwt_service.get_token_subject(jwt_token)
            user = await self.auth_service.get_user_by_username(subject)    
            return user
        except UserNotFoundException:
            raise UserNotFoundException(f"User '{subject}' not found.")
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Invalid access token: {str(e)}")
    
    async def generate_access_token_from_refresh(self, jwt_dto: JWTTokenDTO):
        """ Генерирует новый access-токен на основе валидного refresh-токена. """
        try:
            self.jwt_service.validate_token_type(
                jwt_token=jwt_dto.token, 
                token_type=config_manager.jwt.REFRESH_TOKEN_TYPE
            )
            subject = self.jwt_service.get_token_subject(jwt_dto.token)
            access_token = self.jwt_service.create_access_token(subject)
            return access_token
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Failed to generate access token: {str(e)}")
