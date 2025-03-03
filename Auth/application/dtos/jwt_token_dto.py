from pydantic import BaseModel


class JWTTokensDTO(BaseModel):
    access_token: str | bytes
    refresh_token: str | bytes


class JWTTokenDTO(BaseModel):
    token: str
