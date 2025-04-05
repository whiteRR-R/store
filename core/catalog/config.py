import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent


class DatabaseSettings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL")


class RabbitMQSettings(BaseModel):
    ...

class ConfigManager(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()

config_manager = ConfigManager()
