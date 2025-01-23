from pydantic import BaseModel


class UserLoginRequest(BaseModel):
    username: str
    password: bytes


class UserLoginResponse(BaseModel):
    username: str
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
