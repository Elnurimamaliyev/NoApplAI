"""
Simplified Configuration - Only Essential Settings
"""
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Minimal application settings"""
    
    # App
    APP_NAME: str = "NoApplAI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Database (Required)
    DATABASE_URL: str
    
    # Redis (Required)
    REDIS_URL: str
    
    # JWT (Required)
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Optional
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    LOG_LEVEL: str = "INFO"
    
    def get_cors_origins_list(self):
        """Convert CORS string to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


# Initialize settings
settings = Settings()
