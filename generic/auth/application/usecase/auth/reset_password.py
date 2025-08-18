from application.dtos.reset_password_dto import ResetPasswordDTO
from application.exceptions import TokenProcessingException, UserNotFoundException
from application.interfaces.security.password_security import PasswordSecurityProtocol
from domain.interface.repository.auth_repository import AuthRepositoryProtocol
from domain.interface.repository.redis_repository import RedisRepositoryProtocol
from domain.interface.transaction_manager.transaction_manager import TransactionManager


class ResetPasswordInteractor:
    def __init__(self, 
    auth_repository: AuthRepositoryProtocol, 
    redis_repository: RedisRepositoryProtocol, 
    password_security: PasswordSecurityProtocol,
    transaction_manager: TransactionManager
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

            hashed_password = self.password_security.get_hash_password(reset_dto.new_password.encode())
            user.change_password(hashed_password)
            await self.auth_repository.update(user)
            await self.transaction_manager.commit()
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Invalid reset token: {str(e)}")
