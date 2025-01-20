import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv()


class DatabaseSettings:
    database_url: str = os.getenv("DATABASE_URL")


class JWTSecuritySettings:
    private_key: Path = BASE_DIR / "certs" / "private_key.pem"
    public_key: Path = BASE_DIR / "certs" / "public_key.pem"
    alghoritm: str = "RS256"


class ConfigManager:
    database_settings: DatabaseSettings = DatabaseSettings()
    jwt_settings: JWTSecuritySettings = JWTSecuritySettings()


config_manager = ConfigManager()