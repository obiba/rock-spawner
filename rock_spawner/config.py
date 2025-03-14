from pydantic_settings import BaseSettings
from functools import lru_cache

class Config(BaseSettings):
    API_KEYS: str
    NAMESPACE: str = "default"
    APP_IMAGE: str = "obiba/rock:latest"
    APP_PORT: int = 8085

@lru_cache()
def get_config():
    return Config()

_config = get_config()