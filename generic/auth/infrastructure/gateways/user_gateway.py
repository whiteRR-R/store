import httpx
from application.dtos.user_dto import UserGatewayDTO


class UserHttpGateway:
    def __init__(self, url: str, client: httpx.AsyncClient):
        self.url = url
        self.client = client

    async def create_user(self, user_dto: UserGatewayDTO) -> dict:
        payload = {
            "user_id": str(user_dto.user_id),
            "username": user_dto.username,
            "email": user_dto.email,
            "hashed_password": user_dto.hashed_password.decode(),
            "role": user_dto.role,
            "status": "active"
        }
        response = await self.client.post(f"{self.url}/api/v1/users/users", json=payload)
        response.raise_for_status()
        return response.json()
