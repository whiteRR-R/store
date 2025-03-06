from pydantic import BaseModel


class UserDTO(BaseModel):
    username: str
    email: str
    password: bytes
    role: str = 'user'
