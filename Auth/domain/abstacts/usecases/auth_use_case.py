from abc import ABC, abstractmethod


class AuthUseCaseInterface(ABC):
    @abstractmethod
    async def register(self, username: str, role: str, email: str, password: str):
        raise NotImplementedError
    
    @abstractmethod
    async def login(self, username: str, password: str):
        raise NotImplementedError
    