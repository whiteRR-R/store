from dishka import Provider, Scope, provide

from domain.interface.services.jwt_service import JWTServiceProtocol
from application.interfaces.security.password_security import PasswordSecurityProtocol
from infrastructure.services.jwt_service import JWTService
from infrastructure.security.password_security import PasswordSecurity


class ServicesProvider(Provider):
    scope = Scope.APP

    password_service = provide(PasswordSecurity, provides=PasswordSecurityProtocol)
    jwt_service = provide(JWTService, provides=JWTServiceProtocol)
