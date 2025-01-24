from abc import ABC,abstractmethod


class PasswordSecurityInterface(ABC):
    @abstractmethod
    def get_hash_password(self, password: bytes) -> bytes:
        raise NotImplementedError
    
    @abstractmethod
    def verify_password(self, password: bytes, stored_hash: bytes) -> bool:
        raise NotImplementedError