from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field

class Settings(BaseSettings):
    API_KEY: str = Field(default="29vfjjv9vj9d9324j914a3y2")
    ENV: str = Field(default="development")
    PORT: int = Field(default=8000)

    model_config = ConfigDict(
        env_file = ".env",
        extra = "allow"  # Allow extra fields
    )

settings = Settings()