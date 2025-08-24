import httpx
from dishka import Provider, Scope, provide

from application.interfaces.gateways.user_gateway import UserGateway
from infrastructure.gateways.user_gateway import UserHttpGateway


class GatewayProvider(Provider):
    def __init__(self, url: str):
        super().__init__()
        self.url = url

    @provide(scope=Scope.REQUEST, provides=httpx.AsyncClient)
    async def httpx_client(self):
        async with httpx.AsyncClient() as client:
            yield client

    @provide(scope=Scope.REQUEST, provides=UserGateway)
    def user_gateway(self, client: httpx.AsyncClient) -> UserHttpGateway:
        return UserHttpGateway(self.url, client)

