from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    base_url: str = "http://localhost:7272"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()