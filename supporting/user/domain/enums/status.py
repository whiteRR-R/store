from enum import Enum


class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"
    
    def __repr__(self):
        return self.value
