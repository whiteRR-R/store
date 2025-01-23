from pydantic import BaseModel


class UserRegisterRequest(BaseModel):
    username: str
    role: str = "user"
    email: str
    password: bytes
    

class UserRegisterResponse(BaseModel):
    message: str = "User successful registred"
