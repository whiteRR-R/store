from pydantic import BaseModel


class JWTTokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None
