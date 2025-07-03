from dependency_injector import containers, providers
from domain.entities.user import User
from presentation.controllers.auth_controller import AuthController
from application.usecase.auth_usecase import AuthUseCase
from application.services.auth_service import AuthService
from infrastructure.persistence.data_mapper.user_datamapper import UserDataMapper
from infrastructure.persistence.repository.auth_repository import SQLAlchemyAuthRepository
from infrastructure.persistence.database import Database
from infrastructure.services.jwt_service import JWTService
from infrastructure.persistence.uow.uow import UnitOfWork
from infrastructure.security.password_security import PasswordSecurity
from config import config_manager


class Container(containers.DeclarativeContainer):
    database = providers.Singleton(Database, database_url=config_manager.database.DATABASE_URL)
    session = providers.Factory(database.provided.get_session)
    
    user_datamapper = providers.Singleton(UserDataMapper)
    auth_repository = providers.Factory(SQLAlchemyAuthRepository, session_context_manager=session, user_data_mapper=user_datamapper)    

    password_security = providers.Singleton(PasswordSecurity)

    jwt_service = providers.Singleton(JWTService)
    auth_service = providers.Factory(
        AuthService,
        auth_repository=auth_repository,
        password_security=password_security,
        jwt_service=jwt_service,
    )

    auth_usecase = providers.Factory(AuthUseCase, auth_service=auth_service, jwt_service=jwt_service)
    auth_controller = providers.Factory(AuthController, auth_usecase=auth_usecase)
