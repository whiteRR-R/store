from config import config_manager
from application.dtos.change_email import ChangeEmailDTO
from application.exceptions import UserNotFoundException, EmailAlreadyExistsException, TokenProcessingException
from domain.interface.transaction_manager.transaction_manager import TransactionManager
from domain.valueobject.email import Email
from domain.interface.repository.auth_repository import AuthRepositoryProtocol
from domain.interface.services.jwt_service import JWTServiceProtocol


class UpdateEmailInteractor:
    def __init__(
        self, 
        auth_repository: AuthRepositoryProtocol, 
        jwt_service: JWTServiceProtocol,
        transaction_manager: TransactionManager
    ):
        self.auth_repository = auth_repository
        self.jwt_service = jwt_service
        self.transaction_manager = transaction_manager

    async def execute(self, jwt_token: str, dto: ChangeEmailDTO):
        try:
            self.jwt_service.validate_token_type(jwt_token, config_manager.jwt.ACCESS_TOKEN_TYPE)
            username = self.jwt_service.get_token_subject(jwt_token)

            user = await self.auth_repository.get_by_username(username)
            if not user:
                raise UserNotFoundException(username)
            if await self.auth_repository.get_by_email(dto.new_email):
                raise EmailAlreadyExistsException(dto.new_email)

            new_email = Email(dto.new_email)
            user.change_email(new_email)
            await self.auth_repository.update(user)
            await self.transaction_manager.commit()
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Invalid reset token: {str(e)}")
