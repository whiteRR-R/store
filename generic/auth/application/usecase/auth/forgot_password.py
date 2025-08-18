from uuid import uuid4
from application.dtos.forgot_password_dto import ForgotPasswordDTO
from application.exceptions import UserNotFoundException
from domain.interface.repository.auth_repository import AuthRepositoryProtocol
from domain.interface.repository.redis_repository import RedisRepositoryProtocol


class ForgotPasswordInteractor:
    def __init__(self, auth_repository: AuthRepositoryProtocol, redis_repository: RedisRepositoryProtocol):
        self.auth_repository = auth_repository
        self.redis_repository = redis_repository

    async def execute(self, forgot_dto: ForgotPasswordDTO):
        user = await self.auth_repository.get_by_email(forgot_dto.email)
        if not user:
            raise UserNotFoundException(f"User with email '{forgot_dto.email}' not found.")

        reset_key = uuid4().hex
        await self.redis_repository.set(f"reset_password:{reset_key}", user.username)
        return reset_key
