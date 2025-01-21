from pydantic import BaseModel


class JWTTokens(BaseModel):
    access_token: str | bytes
    refresh_token: str | bytes