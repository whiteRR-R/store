from pydantic import BaseModel


class UserDTO(BaseModel):
    username: str
    email: str
    password: str
    role: str = 'user'
