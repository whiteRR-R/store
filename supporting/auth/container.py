from dependency_injector import containers, providers
from domain.entities.user import User
from presentation.controllers.auth_controller import AuthController
from application.usecase.auth_usecase import AuthUseCase
from infrastructure.persistence.data_mapper.user_datamapper import UserDataMapper
from infrastructure.persistence.redis_client import get_client
from infrastructure.persistence.repository.auth_repository import SQLAlchemyAuthRepository
from infrastructure.persistence.repository.redis_repository import RedisRepository
from infrastructure.persistence.database import Database
from infrastructure.services.jwt_service import JWTService
from infrastructure.security.password_security import PasswordSecurity
from config import config_manager


class Container(containers.DeclarativeContainer):
    database = providers.Singleton(Database, database_url=config_manager.database.URL)

    
    session = providers.Factory(database.provided.get_session)
    redis_client = providers.Resource(
        get_client, 
        redis_port=config_manager.redis.PORT,
        redis_host=config_manager.redis.HOST,
        redis_password=config_manager.redis.PASSWORD
    )

    user_datamapper = providers.Singleton(UserDataMapper)
    auth_repository = providers.Factory(SQLAlchemyAuthRepository, session_context_manager=session, user_datamapper=user_datamapper)
    redis_repository = providers.Singleton(RedisRepository, redis_client=redis_client)    

    password_security = providers.Singleton(PasswordSecurity)

    jwt_service = providers.Singleton(JWTService)
    auth_usecase = providers.Factory(AuthUseCase, auth_repository=auth_repository, redis_repository=redis_repository, password_security=password_security, jwt_service=jwt_service)
    auth_controller = providers.Factory(AuthController, auth_usecase=auth_usecase)
