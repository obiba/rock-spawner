from pydantic_settings import BaseSettings
from functools import lru_cache


class Config(BaseSettings):

    API_KEYS: str


@lru_cache()
def get_config():
    return Config()


config = get_config()