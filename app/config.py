import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "phuc")
    OPENAI_API_BASE: str = os.getenv("OPENAI_API_BASE", "http://0.0.0.0:3637/v1")
    PRIMARY_MODEL: str = "Qwen/Qwen3.5-9B"
    FALLBACK_MODEL: str = "Qwen/Qwen3.5-9B"

    class Config:
        env_file = ".env"

settings = Settings()