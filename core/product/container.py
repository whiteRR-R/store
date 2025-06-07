from dependency_injector import containers, providers
from config import config_manager
from infrastructure.persistence.database import Database
from infrastructure.persistence.repository.brand_repository import BrandRepository
from infrastructure.persistence.repository.category_repository import CategoryRepository
from infrastructure.persistence.repository.product_repository import ProductRepository
from application.usecases.product.create_product_use_case import CreateProductUseCase
from application.usecases.product.get_all_product_use_case import GetAllProductUseCase
from application.usecases.product.get_by_id_product_use_case import GetByIdProductUseCase
from application.usecases.product.delete_product_use_case import DeleteProductUseCase
from application.usecases.category.create_category_use_case import CreateCategoryUseCase
from application.usecases.category.get_all_category_use_case import GetAllCategoryUseCase
from application.usecases.category.delete_category_use_case import DeleteCategoryUseCase
from application.usecases.brand.create_brand_use_case import CreateBrandUseCase
from application.usecases.brand.get_all_brand_use_case import GetAllBrandUseCase
from application.usecases.brand.delete_brand_use_case import DeleteBrandUseCase
from infrastructure.event_bus.subscriber import EventBusSubscriber
from application.events.handlers.category_create_handler import CategoryCreateHandler


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "presentation.api.endpoints.product",
            "presentation.api.endpoints.brand",
            "presentation.api.endpoints.category",
        ]
    )

    database = providers.Singleton(Database, database_url=config_manager.database.URL)
    session = providers.Factory(database.provided.get_session)

    brand_repository = providers.Factory(BrandRepository, session_context_manager=session)
    category_repository = providers.Factory(CategoryRepository, session_context_manager=session)
    product_repository = providers.Factory(ProductRepository, session_context_manager=session)
    

    event_bus_subscriber = providers.Singleton(
        EventBusSubscriber,
        url=config_manager.rabbitmq.URL,
        exchange_name=config_manager.rabbitmq.EXCHANGE_NAME,
        queue_name=config_manager.rabbitmq.QUEUE_NAME,
    ) # type: ignore

    category_create_handler = providers.Singleton(
        CategoryCreateHandler,
        category_repository=category_repository,
    )

    # Use Cases
    create_product_use_case = providers.Factory(
        CreateProductUseCase,
        product_repository=product_repository,
        category_repository=category_repository,
        brand_repository=brand_repository,
    )
    
    get_all_product_use_case = providers.Factory(
        GetAllProductUseCase,
        product_repository=product_repository,
    )
    
    get_by_id_product_use_case = providers.Factory(
        GetByIdProductUseCase,
        product_repository=product_repository,
    )
    
    delete_product_use_case = providers.Factory(
        DeleteProductUseCase,
        product_repository=product_repository,
    )
    
    create_category_use_case = providers.Factory(
        CreateCategoryUseCase,
        category_repository=category_repository,
    )
    
    get_all_category_use_case = providers.Factory(
        GetAllCategoryUseCase,
        category_repository=category_repository,
    )
    
    delete_category_use_case = providers.Factory(
        DeleteCategoryUseCase,
        category_repository=category_repository,
    )
    
    create_brand_use_case = providers.Factory(
        CreateBrandUseCase,
        brand_repository=brand_repository,
    )
    
    get_all_brand_use_case = providers.Factory(
        GetAllBrandUseCase,
        brand_repository=brand_repository,
    )
    
    delete_brand_use_case = providers.Factory(
        DeleteBrandUseCase,
        brand_repository=brand_repository,
    )
