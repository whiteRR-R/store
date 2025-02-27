from pydantic import BaseModel


class UserDataResponse(BaseModel):
    username: str
    email: str 
    role: str
