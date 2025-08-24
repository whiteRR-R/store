from dishka import Provider, Scope, provide

from domain.interface.services.jwt_service import JWTServiceProtocol
from domain.interface.services.hash_service import PasswordHasherProtocol
from infrastructure.services.jwt_service import JWTService
from infrastructure.services.security.password_security import BcryptPasswordHasher


class ServicesProvider(Provider):
    scope = Scope.APP

    password_service = provide(BcryptPasswordHasher, provides=PasswordHasherProtocol)
    jwt_service = provide(JWTService, provides=JWTServiceProtocol)
