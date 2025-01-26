from domain.entities.user import User
from abc import abstractmethod, ABC


class AuthServiceInterface(ABC):
    @abstractmethod
    async def create_user(self, user: User):
        raise NotImplementedError
    
    @abstractmethod
    async def existing_username_and_email(self, username: str, email: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def verify_user_credentials(self, username: str, password: str):
        raise NotImplementedError
    
    
