from dependency_injector import containers, providers
from domain.entities.user import User
from presentation.controllers.auth_controller import AuthController
from application.usecase.auth_usecase import AuthUseCase
from application.services.auth_service import AuthService
from infrastructure.persistence.data_mapper.user_datamapper import UserDataMapper
from infrastructure.persistence.repository.auth_repository import AuthRepository
from infrastructure.persistence.database import Database
from infrastructure.services.jwt_service import JWTService
from infrastructure.persistence.uow.uow import UnitOfWork
from infrastructure.security.password_security import PasswordSecurity
from config import config_manager


class Container(containers.DeclarativeContainer):
    database = providers.Singleton(Database, database_url=config_manager.database.DATABASE_URL)

    session = providers.Resource(database.provided.session_factory)
    
    auth_repository = providers.Factory(AuthRepository, session=session)
    user_datamapper = providers.Factory(UserDataMapper, session=session)
    mappers = providers.Dict({User: user_datamapper})
    
    unit_of_work = providers.Factory(UnitOfWork, session=session, mappers=mappers)
    

    password_security = providers.Singleton(PasswordSecurity)

    jwt_service = providers.Singleton(JWTService)
    auth_service = providers.Factory(
        AuthService,
        auth_repository=auth_repository,
        unit_of_work=unit_of_work,
        password_security=password_security,
        jwt_service=jwt_service,
    )

    auth_usecase = providers.Factory(AuthUseCase, auth_service=auth_service, jwt_service=jwt_service)
    auth_controller = providers.Factory(AuthController, auth_usecase=auth_usecase)
