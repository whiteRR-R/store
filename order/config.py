from pydantic_settings import BaseSettings, SettingsConfigDict


class Database(BaseSettings):
    URL: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="POSTGRES_DATABASE_",
        extra="ignore"
    )


class ConfigManager:
    def __init__(self):
        self.database = Database()


config_manager = ConfigManager()

print(config_manager.database.URL)
