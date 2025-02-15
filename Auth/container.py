from dependency_injector import containers, providers
from config import config_manager
from presentation.controllers.auth_controller import AuthController
from application.usecase.auth_usecase import AuthUseCase
from application.services.auth_service import AuthService
from infrastructure.persistence.database import Database
from infrastructure.services.jwt_service import JWTService
from infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork
from infrastructure.security.jwt_security import JWTSecurity
from infrastructure.security.password_security import PasswordSecurity


class Container(containers.DeclarativeContainer):
    database = providers.Singleton(Database, database_url=config_manager.database.DATABASE_URL)
    
    # Асинхронный ресурс для работы сессии
    session = providers.Resource(lambda database: database.get_session(), database=database)
    print(session)
    print(type(session))
    sqlalchemy_uow = providers.Factory(
        SqlAlchemyUnitOfWork,
        session=session,  # Передаем провайдер ресурса session
    )
    
    jwt_security = providers.Singleton(JWTSecurity)
    password_security = providers.Singleton(PasswordSecurity)
    
    jwt_service = providers.Factory(JWTService, jwt_security=jwt_security)
    auth_service = providers.Factory(
        AuthService,
        uow=sqlalchemy_uow,
        password_security=password_security,
        jwt_service=jwt_service,
    )
    
    auth_usecase = providers.Factory(AuthUseCase, auth_service=auth_service, jwt_service=jwt_service)
    auth_controller = providers.Factory(AuthController, auth_usecase=auth_usecase)
