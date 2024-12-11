from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    API_KEY: str = "test-key-123"
    ENV: str = "development"

    model_config = ConfigDict(
        env_file = ".env"
    )

settings = Settings()