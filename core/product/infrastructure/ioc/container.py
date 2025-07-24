from dishka import make_async_container
from infrastructure.ioc.providers.database import DatabaseProvider
from infrastructure.ioc.providers.repository import RepositoryProvider
from infrastructure.ioc.providers.s3_storage import S3Provider
from infrastructure.ioc.providers.use_cases import UseCaseProvider
from config import config_manager


def create_container():
    return make_async_container(
        DatabaseProvider(config_manager.database.URL),
        RepositoryProvider(),
        UseCaseProvider(),
        S3Provider(
            bucket_name=config_manager.s3.BUCKET_NAME,
            endpoint_url=config_manager.s3.ENDPOINT_URL,
            access_key=config_manager.s3.AWS_ACCESS_KEY_ID,
            secret_key=config_manager.s3.AWS_SECRET_ACCESS_KEY,
        )
    )
