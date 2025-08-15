from dishka import Provider, Scope, provide
from domain.interfaces.repositories.address_repository import AddressRepository
from domain.interfaces.repositories.user_repository import UserRepository
from infrastructure.persistence.repositories.address_repository import SQLAlchemyAddressRepository
from infrastructure.persistence.repositories.user_repository import SQLAlchemyUserRepository


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    user_repository = provide(SQLAlchemyUserRepository, provides=UserRepository)
    address_repository = provide(SQLAlchemyAddressRepository, provides=AddressRepository)
