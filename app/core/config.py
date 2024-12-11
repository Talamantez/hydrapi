from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_KEY: str = "test-key-123"
    ENV: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()