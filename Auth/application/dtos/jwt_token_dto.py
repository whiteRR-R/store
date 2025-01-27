from pydantic import BaseModel


class JWTTokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class JWTTokens(BaseModel):
    access_token: str | bytes
    refresh_token: str | bytes
    