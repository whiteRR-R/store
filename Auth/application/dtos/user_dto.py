from pydantic import BaseModel


class UserDataResponse(BaseModel):
    username: str
    role: str
    email: str
    