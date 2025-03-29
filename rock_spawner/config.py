from pydantic_settings import BaseSettings
from functools import lru_cache

class Config(BaseSettings):
    API_KEYS: str
    NAMESPACE: str = "default"
    APP_BASENAME: str = "rock"
    APP_IMAGE: str = "obiba/rock:latest"
    APP_PORT: int = 8085
    ROCK_CLUSTER: str = "kubernetes"
    ROCK_ADMINISTRATOR_NAME: str = ""
    ROCK_ADMINISTRATOR_PASSWORD: str = ""
    ROCK_MANAGER_NAME: str = ""
    ROCK_MANAGER_PASSWORD: str = ""
    ROCK_USER_NAME: str = ""
    ROCK_USER_PASSWORD: str = ""
    
@lru_cache()
def get_config():
    return Config()

_config = get_config()