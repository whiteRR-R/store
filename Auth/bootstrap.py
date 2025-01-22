from config import config_manager
from presentation.http.controllers.auth_controller import AuthController
from application.usecase.auth_usecase import AuthUseCase
from application.services.auth_service import AuthService
from infrastructure.persistence.database import Database
from infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork
from infrastructure.security.jwt_security import JWTSecurity
from infrastructure.security.password_security import PasswordSecurity


def initializate_auth_controller():
    database = Database(config_manager.database_settings.database_url)
    sql_alchemy_uow = SqlAlchemyUnitOfWork(database._session_factory)
    password_security_service = PasswordSecurity()
    jwt_security_service = JWTSecurity()
    auth_service = AuthService(sql_alchemy_uow, password_security_service, jwt_security_service)
    auth_usecase = AuthUseCase(auth_service)
    auth_controller = AuthController(auth_usecase)
    
    return auth_controller
    