from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Sentinel Backend"
    environment: str = "development"
    
    # TODO: Add configuration for database, LLM keys, etc.

    class Config:
        env_file = ".env"

settings = Settings()
