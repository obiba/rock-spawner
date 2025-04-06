from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import Field
from functools import lru_cache

class Config(BaseSettings):
    API_KEYS: str
    NAMESPACE: str = "default"
    APP_BASENAME: str = "rock"
    APP_IMAGE: str = "obiba/rock:latest"
    APP_PORT: int = 8085
    APP_MEMORY_REQUEST: Optional[str] = Field(default=None) # e.g. 512Mi
    APP_MEMORY_LIMIT: Optional[str] = Field(default=None) # e.g. 512Mi
    APP_CPU_REQUEST: Optional[str] = Field(default=None) # e.g. 500m
    APP_CPU_LIMIT: Optional[str] = Field(default=None) # e.g. 500m
    APP_SERVICE: Optional[str] = Field(default=None) # ClusterIP, NodePort, LoadBalancer
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