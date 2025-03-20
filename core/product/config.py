import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig(BaseModel):
    DATABASE_URL = os.getenv("DATABASE_URL", "")


class ConfigManager(BaseSettings):
    database: DatabaseConfig = DatabaseConfig()


config_manager = ConfigManager()