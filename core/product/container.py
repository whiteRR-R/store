from application.usecases.product.create_product_use_case import CreateProductUseCase
from application.usecases.product.delete_product_use_case import DeleteProductUseCase
from application.usecases.product.get_all_product_use_case import GetAllProductUseCase
from application.usecases.product.get_by_id_product_use_case import GetByIdProductUseCase
from application.usecases.category.create_category_use_case import CreateCategoryUseCase
from application.usecases.category.delete_category_use_case import DeleteCategoryUseCase
from application.usecases.category.get_all_category_use_case import GetAllCategoryUseCase
from application.usecases.brand.create_brand_use_case import CreateBrandUseCase
from application.usecases.brand.get_all_brand_use_case import GetAllBrandUseCase
from application.usecases.brand.delete_brand_use_case import DeleteBrandUseCase
from application.events.handlers.category_create_handler import CategoryCreateHandler
from infrastructure.event_bus.subscriber import EventBusSubscriber
from infrastructure.persistence.repository.brand_repository import BrandRepository
from infrastructure.persistence.repository.category_repository import CategoryRepository
from infrastructure.persistence.repository.product_repository import ProductRepository
from infrastructure.persistence.database import Database
from dependency_injector import containers, providers

from config import config_manager


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "presentation.api.endpoints.product",
            "presentation.api.endpoints.brand",
        ]
    )
    # Database
    database = providers.Singleton(Database, database_url=config_manager.database.URL)
    
    # Repository
    brand_repository = providers.Factory(BrandRepository, session=providers.Dependency())
    category_repository = providers.Factory(CategoryRepository, session=providers.Dependency())
    product_repository = providers.Factory(ProductRepository, session=providers.Dependency())
    
    # Event Bus
    event_bus_subscriber = providers.Singleton( 
        EventBusSubscriber,
        url=config_manager.rabbitmq.URL,
        exchange_name=config_manager.rabbitmq.EXCHANGE_NAME,
        queue_name=config_manager.rabbitmq.QUEUE_NAME,
    ) # type: ignore
    
    # Event Handlers
    category_create_handler = providers.Singleton(
        CategoryCreateHandler,
        category_repository=category_repository,
    )
    
    # Product Use Cases
    create_product_use_case = providers.Singleton(
        CreateProductUseCase,
        product_repository=product_repository,
        category_repository=category_repository,
        brand_repository=brand_repository,
    )
    
    delete_product_use_case = providers.Singleton(
        DeleteProductUseCase,
        product_repository=product_repository,
    )
    get_all_product_use_case = providers.Singleton(
        GetAllProductUseCase,
        product_repository=product_repository,
    )
    get_by_id_product_use_case = providers.Singleton(
        GetByIdProductUseCase,
        product_repository=product_repository,
    )
    
    # Category Use Cases
    create_category_use_case = providers.Singleton(
        CreateCategoryUseCase,
        category_repository=category_repository
    )
    
    delete_category_use_case = providers.Singleton(
        DeleteCategoryUseCase,
        category_repository=category_repository
    ) 
    
    get_all_category_use_case = providers.Singleton(
        GetAllCategoryUseCase,
        category_repository=category_repository
    )
    
    # Brand Use Cases
    create_brand_use_case = providers.Singleton(
        CreateBrandUseCase,
        brand_repository=brand_repository,
    )
    
    get_all_brand_use_case = providers.Singleton(
        GetAllBrandUseCase,
        brand_repository=brand_repository,
    )
    
    delete_brand_use_case = providers.Singleton(
        DeleteBrandUseCase,
        brand_repository=brand_repository,
    )
    
    
    
    

    
    
