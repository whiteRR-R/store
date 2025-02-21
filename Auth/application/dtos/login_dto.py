from dataclasses import dataclass

@dataclass(frozen=True)
class UserLoginDTO:
    username: str
    password: str
