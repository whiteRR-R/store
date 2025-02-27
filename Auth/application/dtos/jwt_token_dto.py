from dataclasses import dataclass


@dataclass(frozen=True)
class JWTTokensDTO:
    access_token: str | bytes
    refresh_token: str | bytes


@dataclass(frozen=True)
class JWTTokenDTO:
    token: str
