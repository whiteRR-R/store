from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from domain.interface.repository.redis_repository import RedisRepositoryProtocol
from domain.interface.repository.auth_repository import AuthRepositoryProtocol
from infrastructure.persistence.repository.auth_repository import SQLAlchemyAuthRepository
from infrastructure.persistence.repository.redis_repository import RedisRepository


class RepositoryProvider(Provider):
    def __init__(self, redis_url: str):
        super().__init__()
        self._redis_url = redis_url

    @provide(scope=Scope.REQUEST, provides=AuthRepositoryProtocol)
    def auth_repository(self, session: AsyncSession) -> SQLAlchemyAuthRepository:
        return SQLAlchemyAuthRepository(session)

    @provide(scope=Scope.REQUEST, provides=RedisRepositoryProtocol)
    def redis_repository(self) -> RedisRepositoryProtocol:
        return RedisRepository(self._redis_url)
