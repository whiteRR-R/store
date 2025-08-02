from dishka import Provider, Scope, provide
from domain.interfaces.storages.s3_image_storage import S3ImageStorageProtocol
from infrastructure.storage.s3_storage import S3ImageStorage


class S3Provider(Provider):
    def __init__(
        self,
        bucket_name: str,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
    ):
        super().__init__()
        self._bucket_name = bucket_name
        self._endpoint_url = endpoint_url
        self._access_key = access_key
        self._secret_key = secret_key

    @provide(scope=Scope.APP, provides=S3ImageStorageProtocol)
    def provide_s3_storage(self) -> S3ImageStorage:
        return S3ImageStorage(
            bucket_name=self._bucket_name,
            endpoint_url=self._endpoint_url,
            access_key=self._access_key,
            secret_key=self._secret_key,
        )
