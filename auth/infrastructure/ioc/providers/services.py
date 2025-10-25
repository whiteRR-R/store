from dishka import Provider, Scope, provide

from application.interfaces.security.token_provider import TokenProviderProtocol
from domain.interface.services.hash_service import PasswordHasherProtocol
from infrastructure.services.security.jwt_service import JWTService
from infrastructure.services.security.password_service import BcryptPasswordHasher


class ServicesProvider(Provider):
    scope = Scope.APP

    password_service = provide(BcryptPasswordHasher, provides=PasswordHasherProtocol)
    jwt_service = provide(JWTService, provides=TokenProviderProtocol)
