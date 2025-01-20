from abc import ABC, abstractmethod


class JWTSecurityInterface(ABC):
    @abstractmethod
    def encode_jwt(self):
        raise NotImplementedError
    
    @abstractmethod
    def decode_jwt(self):
        raise NotImplementedError
    