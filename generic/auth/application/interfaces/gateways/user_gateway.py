from typing import Protocol
from uuid import UUID

from application.dtos.user_dto import UserGatewayDTO


class UserGateway(Protocol):
    async def create_user(self, user_dto: UserGatewayDTO) -> dict: ...
    
    async def get_user(self, user_id: UUID) -> dict: ...
