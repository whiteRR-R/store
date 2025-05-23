from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    NAME: str
    HOST: str
    PORT: int
    USER: str
    PASS: str
    URL: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="PRODUCT_POSTGRES_",
        extra="ignore",
    )


class RabbitMQSettings(BaseSettings):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    URL: str
    EXCHANGE_NAME: str
    QUEUE_NAME: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="RABBITMQ_",
        extra="ignore",
    )


class ConfigManager:
    def __init__(self):
        self.database = DatabaseSettings()
        self.rabbitmq = RabbitMQSettings()


config_manager = ConfigManager()
