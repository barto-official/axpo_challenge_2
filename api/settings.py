from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache

class MySQLSettings(BaseSettings):
    class Config:
        env_file = '.env'
        env_prefix = 'MYSQL_'

    user: str
    password: str
    host: str
    database: str

class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    mysql: MySQLSettings = MySQLSettings()
    interval_ms: int = 1000
    logging_level: int = 30

@lru_cache()
def get_settings() -> Settings:
    return Settings()
