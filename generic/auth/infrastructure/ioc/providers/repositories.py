from dishka import Provider, Scope, provide

from domain.interface.repository.redis_repository import RedisRepositoryProtocol
from domain.interface.repository.auth_repository import AuthRepositoryProtocol
from infrastructure.persistence.repository.auth_repository import SQLAlchemyAuthRepository
from infrastructure.persistence.repository.redis_repository import RedisRepository


class RepositoryProvider(Provider):
    scope = Scope.REQUEST
    auth_repository = provide(SQLAlchemyAuthRepository, provides=AuthRepositoryProtocol)
    redis_repository = provide(RedisRepository, provides=RedisRepositoryProtocol)
