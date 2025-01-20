from domain.interface.services.auth_service import AuthServiceInterface


class AuthUseCase:
    def __init__(self, auth_service: AuthServiceInterface):
        self.auth_service = auth_service
    
    async def register(self, username: str, role: str, email: str, password: str):
        await self.auth_service.register_user(
            username=username, role=role, email=email, password=password
        )
    
    async def login(self, username: str, password: str):
        try:
            await self.auth_service.login_user(username=username, password=password)
        except Exception:
            raise ValueError("Invalid credentials")
