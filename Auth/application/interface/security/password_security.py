from typing import Protocol

class PasswordSecurityProtocol(Protocol):
    def get_hash_password(self, password: bytes) -> bytes:
        ...
    
    def verify_password(self, password: bytes, stored_hash: bytes) -> bool:
        ...
