import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv()


class DatabaseSettings:
    database_url: str = os.getenv("DATABASE_URL")


class JWTSettings:
    private_key: Path = BASE_DIR / "certs" / "private_key.pem"
    public_key: Path = BASE_DIR / "certs" / "public_key.pem"
    alghoritm: str = "RS256"
    reset_token_expire_time_minute = 10
    access_token_expire_time_minute = 15
    refresh_token_expire_time_day = 20
    reset_token_type = 'reset'
    access_token_type = 'access'
    refresh_token_type = 'refresh'


class ConfigManager:
    database_settings: DatabaseSettings = DatabaseSettings()
    jwt_settings: JWTSettings = JWTSettings()


config_manager = ConfigManager()