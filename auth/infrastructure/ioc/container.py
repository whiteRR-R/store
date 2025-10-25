from dishka import make_async_container
from infrastructure.ioc.providers.database import DatabaseProvider
from infrastructure.ioc.providers.repositories import RepositoryProvider
from infrastructure.ioc.providers.services import ServicesProvider
from infrastructure.ioc.providers.interactors import InteractorProvider
from infrastructure.ioc.providers.gateways import GatewayProvider
from config import config_manager

def create_container():
    return make_async_container(
        DatabaseProvider(),
        RepositoryProvider(config_manager.redis.URL),
        ServicesProvider(),
        InteractorProvider(),
        GatewayProvider("http://localhost:8001")
)
