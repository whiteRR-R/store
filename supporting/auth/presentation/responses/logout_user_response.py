from pydantic import BaseModel


class LogoutUserResponse(BaseModel):
    message: str
