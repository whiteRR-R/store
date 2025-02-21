from dataclasses import dataclass

@dataclass(frozen=True)
class UserDTO:
    username: str
    email: str
    password: str
    role: str = 'user'
