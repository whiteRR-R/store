from dependency_injector import containers, providers
from presentation.controllers.category_contoller import CategoryController
from application.services.category_service import CategoryService
from infrastructure.persistence.database import SQLAlchemyDatabase
from infrastructure.persistence.repository.category import CategoryRepository
from infrastructure.persistence.datamapper.category_mapper import CategoryDataMapper
from infrastructure.event_bus.rabbitmq_event_bus import RabbitMQEventBus
from config import config_manager


class Container(containers.Container):
    database = providers.Singleton(SQLAlchemyDatabase, URL=config_manager.database.URL)
    session = providers.Resource(database.provided.session_factory)
    print(session)
    category_repository = providers.Singleton(
        CategoryRepository,
        session=session,
    )
    
    event_bus = providers.Singleton(
        RabbitMQEventBus,
        host=config_manager.rabbitmq.HOST,
        exchange_name=config_manager.rabbitmq.EXCHANGE_NAME,
        queue_name=config_manager.rabbitmq.QUEUE_NAME,
        )
    
    category_service = providers.Singleton(
        CategoryService,
        category_repository=category_repository,
        event_bus=event_bus,
    )
    category_controller = providers.Factory(
        CategoryController,
        category_service=category_service,
    )
