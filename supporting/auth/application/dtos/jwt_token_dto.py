from pydantic import BaseModel


class JWTTokensDTO(BaseModel):
    access_token: str
    refresh_token: str


class JWTTokenDTO(BaseModel):
    token: str
