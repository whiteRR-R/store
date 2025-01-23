from pydantic import BaseModel


class UserRegisterRequest(BaseModel):
    username: str
    role: str = "user"
    email: str
    password: str
    

class UserRegisterResponse(BaseModel):
    message: str = "User successful registred"
