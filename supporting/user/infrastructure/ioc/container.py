from dishka import make_async_container
from infrastructure.ioc.providers.database import DatabaseProvider
from infrastructure.ioc.providers.repository import RepositoryProvider
from infrastructure.ioc.providers.usecase import UseCaseProvider

def create_container():
    return make_async_container(
        DatabaseProvider("postgresql+asyncpg://account_user:secret_password@localhost:5434/postgres"),
        RepositoryProvider(),
        UseCaseProvider()
    )
