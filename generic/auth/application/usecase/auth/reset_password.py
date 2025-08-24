from application.dtos.reset_password_dto import ResetPasswordDTO
from application.exceptions import TokenProcessingException, UserNotFoundException
from domain.interface.services.hash_service import PasswordHasherProtocol
from domain.interface.repository.auth_repository import AuthRepositoryProtocol
from domain.interface.repository.redis_repository import RedisRepositoryProtocol
from domain.interface.transaction_manager.transaction_manager import TransactionManagerProtocol


class ResetPasswordInteractor:
    def __init__(self, 
    auth_repository: AuthRepositoryProtocol, 
    redis_repository: RedisRepositoryProtocol, 
    password_security: PasswordHasherProtocol,
    transaction_manager: TransactionManagerProtocol
    ):
        self.auth_repository = auth_repository
        self.redis_repository = redis_repository
        self.password_security = password_security
        self.transaction_manager = transaction_manager

    async def __call__(self, reset_dto: ResetPasswordDTO):
        try:
            if not await self.redis_repository.exists(f"reset_password:{reset_dto.reset_key}"):
                raise TokenProcessingException("Reset key not found in Redis")

            username = await self.redis_repository.getdel(f"reset_password:{reset_dto.reset_key}")
            user = await self.auth_repository.get_by_username(username)
            
            if not user:
                raise UserNotFoundException(username)

            user.set_password(reset_dto.new_password, self.password_security)
            await self.auth_repository.update(user)
            await self.transaction_manager.commit()
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Invalid reset token: {str(e)}")
