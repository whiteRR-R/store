from abc import ABC,abstractmethod


class PasswordSecurityInterface(ABC):
    @abstractmethod
    def get_hash_password(self):
        raise NotImplementedError
    
    @abstractmethod
    def verify_password(self):
        raise NotImplementedError