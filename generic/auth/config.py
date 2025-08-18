from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class DatabaseSettings(BaseSettings):
    URL: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="AUTH_POSTGRES_",
        extra="ignore",
    )

class REDISSettings(BaseSettings):
    URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="REDIS_",
        extra="ignore",
    )

class JWTSettings(BaseSettings):
    PRIVATE_KEY: Path = BASE_DIR / "certs" / "private_key.pem"
    PUBLIC_KEY: Path = BASE_DIR / "certs" / "public_key.pem"
    ALGORITHM: str = "RS256"
    RESET_TOKEN_TYPE: str = 'reset'
    ACCESS_TOKEN_TYPE: str = 'access'
    REFRESH_TOKEN_TYPE: str = 'refresh'
    reset_token_expire_time_minute: int = 10
    access_token_expire_time_minute: int = 15
    refresh_token_expire_time_day: int = 20


class ConfigManager:
    def __init__(self):
        self.database = DatabaseSettings()
        self.jwt = JWTSettings()
        self.redis = REDISSettings()


config_manager = ConfigManager()
