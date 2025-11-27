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
    DATABASE_URL: Optional[str] = None
    
    # Individual DB variables (optional, used to build DATABASE_URL if it's missing)
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_NAME: Optional[str] = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> str:
        if isinstance(v, str) and v:
            return v
        
        # If DATABASE_URL is not set, try to build it from individual components
        # We access other fields via info.data, but note that validation order matters.
        # However, for 'mode="before"', info.data might not be fully populated with validated values yet 
        # if we rely on standard validation order. 
        # A safer approach with pydantic v2 model_validator is often preferred for cross-field validation,
        # but let's try to access the raw values from the environment or defaults if needed, 
        # or use a model_validator after.
        
        return v

    def model_post_init(self, __context):
        """
        Construct DATABASE_URL if it wasn't provided but individual fields were.
        Using model_post_init ensures we have access to all loaded values.
        """
        if self.DATABASE_URL:
            return

        if self.DB_HOST and self.DB_USER and self.DB_NAME:
            # Assume Postgres if individual fields are provided
            password = f":{self.DB_PASSWORD}" if self.DB_PASSWORD else ""
            port = f":{self.DB_PORT}" if self.DB_PORT else ""
            self.DATABASE_URL = f"postgresql://{self.DB_USER}{password}@{self.DB_HOST}{port}/{self.DB_NAME}"
        else:
            # Default to SQLite
            self.DATABASE_URL = "sqlite:///./database.db"

settings = Settings()
