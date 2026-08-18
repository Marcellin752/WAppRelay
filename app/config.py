from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    VERIFY_TOKEN: str
    APP_SECRET: str
    ACCESS_TOKEN: str
    PHONE_NUMBER_ID: int
    RELAY_TARGET_NUMBER: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache
def get_settings():
    return Settings()
