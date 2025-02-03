from abc import ABC, abstractmethod


class AuthUseCaseInterface(ABC):
    @abstractmethod
    async def register(self, username: str, role: str, email: str, password: str):
        raise NotImplementedError
    
    @abstractmethod
    async def login(self, username: str, password: str):
        raise NotImplementedError
    
    @abstractmethod
    async def get_current_user_info(self, jwt_token: str):
        raise NotImplementedError
    
    @abstractmethod
    async def generate_access_token_from_refresh(self, jwt_token: str):
        raise NotImplementedError
    
    @abstractmethod
    async def forgot_password(self, email: str):
        raise NotImplementedError
    
    @abstractmethod
    async def reset_password(self, jwt_token: str, new_password: bytes):
        raise NotImplementedError
    
    