import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent
load_dotenv()


class DatabaseSettings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL")


class JWTSettings(BaseModel):
    PRIVATE_KEY: Path = BASE_DIR / "certs" / "private_key.pem"
    PUBLIC_KEY: Path = BASE_DIR / "certs" / "public_key.pem"
    ALGORITHM: str = "RS256"
    RESET_TOKEN_TYPE: str = 'reset'
    ACCESS_TOKEN_TYPE: str = 'access'
    REFRESH_TOKEN_TYPE: str = 'refresh'
    reset_token_expire_time_minute: int = 10
    access_token_expire_time_minute: int = 15
    refresh_token_expire_time_day: int = 20


class ConfigManager(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()


config_manager = ConfigManager()