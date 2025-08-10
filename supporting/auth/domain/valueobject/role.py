from enum import Enum


class Role(Enum):
    USER = "USER" 
    MANAGER = "MANAGER"
    ADMIN = "ADMIN" 

    def __repr__(self):
        return self.value
