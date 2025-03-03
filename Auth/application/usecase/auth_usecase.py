from domain.interface.services.auth_service import AuthServiceInterface
from domain.interface.services.jwt_service import JWTServiceInterface
from domain.interface.usecases.auth_usecase import AuthUseCaseInterface
from application.interface.security.password_security import PasswordSecurityInterface
from application.dtos.user_dto import UserDTO
from application.dtos.login_dto import UserLoginDTO
from application.dtos.jwt_token_dto import JWTTokenDTO
from application.dtos.forgot_password_dto import ForgotPasswordDTO
from application.dtos.reset_password_dto import ResetPasswordDTO
from application.exceptions import (
    ApplicationException,
    AuthException,
    UserNotFoundException,
    RegistrationException,
    TokenProcessingException,
)
from config import config_manager


class AuthUseCase(AuthUseCaseInterface):
    def __init__(
        self,
        auth_service: AuthServiceInterface,
        jwt_service: JWTServiceInterface,
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
        except RegistrationException as exception:
            raise RegistrationException(f"Registration failed: {str(exception)}")
        
    async def login(self, user_credentials: UserLoginDTO):
        """
        Логин пользователя. Проверяет правильность имени пользователя и пароля а так же создает токены.
        """
        try: 
            await self.auth_service.verify_user_credentials(user_credentials)
            jwt_tokens = await self.jwt_service.generate_jwt_tokens(user_credentials.username)
            return jwt_tokens
        except AuthException as exception:
            raise AuthException(f"Authentication failed: {str(exception)}")
            
    async def forgot_password(self, forgot_dto: ForgotPasswordDTO):
        """ Генерирует reset-токен для сброса пароля """
        try:
            user = await self.auth_service.get_user_by_email(forgot_dto.email)
            payload = {"sub": user.username}
            reset_token = self.jwt_service.create_reset_token(payload)
            #TODO: Добавить отправку ссылку для сброса на почту
            return reset_token
        except UserNotFoundException:
            raise UserNotFoundException("User not found")
        except Exception as exception:
            raise ApplicationException(f"Failed to generate token: {str(exception)}")
    
    async def reset_password(self, reset_dto: ResetPasswordDTO):
        """ Сбросывает пароль через reset-токен """
        try:
            await self.jwt_service.validate_token_type(jwt_token=ResetPasswordDTO.jwt_token, token_type=config_manager.jwt.RESET_TOKEN_TYPE)
            username = await self.jwt_service.get_token_subject(ResetPasswordDTO.jwt_token)
            await self.auth_service.update_password(username, ResetPasswordDTO.new_password)  
        except UserNotFoundException:
            raise UserNotFoundException("User not found for password reset.")
        except Exception as exception:
            raise ApplicationException(f"Unexpected error during password reset: {str(exception)}") 
             
    async def get_current_user_info(self, jwt_dto: JWTTokenDTO):
        """ Возврашает информацию текущего пользователя """
        try:
            await self.jwt_service.validate_token_type(jwt_token=jwt_dto.token, token_type=config_manager.jwt.RESET_TOKEN_TYPE)
            subject_name = await self.jwt_service.get_token_subject(jwt_dto.token)
            user = await self.auth_service.get_user_by_username(subject_name)    
            return user
        except AuthException as exception:
            raise UserNotFoundException(f"User not found: {str(exception)}")
    
    async def generate_access_token_from_refresh(self, jwt_dto: JWTTokenDTO):
        """ Генерирует новый access-токен на основе валидного refresh-токена. """
        try:
            await self.jwt_service.validate_token_type(jwt_token=jwt_dto.token, token_type=config_manager.jwt.RESET_TOKEN_TYPE)
            subject = await self.jwt_service.get_token_subject(jwt_dto.token)
            payload = {"sub": subject}
            access_token = await self.jwt_service.create_access_token(payload)
            return access_token
        except ApplicationException as exception:
            raise TokenProcessingException(f"Failed to generate access token from refresh token: {str(exception)}")
    
