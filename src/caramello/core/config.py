from typing import Optional
from pydantic import PostgresDsn, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_ignore_empty=True, 
        extra="ignore"
    )

    ENVIRONMENT: str = "development"
    
    # Database Configuration
    # We construct the URL from individual components.
    # DATABASE_URL is not read from env directly anymore.
    DATABASE_URL: Optional[str] = None
    
    # Individual DB variables (Required)
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    def model_post_init(self, __context):
        """
        Construct DATABASE_URL from individual fields.
        """
        password = f":{self.DB_PASSWORD}" if self.DB_PASSWORD else ""
        port = f":{self.DB_PORT}" if self.DB_PORT else ""
        self.DATABASE_URL = f"postgresql://{self.DB_USER}{password}@{self.DB_HOST}{port}/{self.DB_NAME}"

settings = Settings()

