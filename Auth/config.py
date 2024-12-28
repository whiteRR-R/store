import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv()


class DatabaseSettings:
    database_url: str = os.getenv("DATABASE_URL")


class ConfigManager:
    database_settings: DatabaseSettings = DatabaseSettings()


config_manager = ConfigManager()