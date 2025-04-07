import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent

class DatabaseSettings(BaseModel):
    URL: str = os.getenv("CATEGORY_DB_URL")


class RabbitMQSettings(BaseModel):
    HOST: str = os.getenv("RABBITMQ_HOST")
    URL: str = os.getenv("RABBITMQ_URL")
    EXCHANGE_NAME: str = os.getenv("RABBITMQ_EXCHANGE_NAME")
    QUEUE_NAME: str = os.getenv("RABBITMQ_QUEUE_NAME")

class ConfigManager(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()

config_manager = ConfigManager()
