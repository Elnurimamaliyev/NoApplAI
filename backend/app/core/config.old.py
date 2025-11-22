"""
NoApplAI Backend Application Configuration
Main configuration module using Pydantic Settings
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import EmailStr, field_validator
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "NoApplAI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str
    REDIS_CACHE_TTL: int = 3600
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # AWS S3
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str
    S3_ENDPOINT_URL: Optional[str] = None
    
    # File Upload
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_FILE_EXTENSIONS: Optional[str] = ".pdf,.jpg,.jpeg,.png,.docx,.doc"
    
    # Email (Optional)
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[str] = None
    MAIL_PORT: int = 587
    MAIL_SERVER: Optional[str] = None
    MAIL_FROM_NAME: str = "NoApplAI Platform"
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
    
    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    
    # OpenAI (Optional)
    OPENAI_API_KEY: Optional[str] = None
    AI_MODEL: str = "gpt-4-turbo-preview"
    AI_MATCH_TEMPERATURE: float = 0.7
    AI_MATCH_MAX_TOKENS: int = 1000
    
    # Sentry
    SENTRY_DSN: Optional[str] = None
    
    # CORS
    CORS_ORIGINS: Optional[str] = "http://localhost:3000,http://localhost:8000,http://localhost:5173"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    def get_cors_origins_list(self) -> List[str]:
        """Parse CORS origins from string to list"""
        if self.CORS_ORIGINS:
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return ["http://localhost:3000", "http://localhost:8000"]
    
    def get_allowed_extensions_list(self) -> List[str]:
        """Parse allowed file extensions from string to list"""
        if self.ALLOWED_FILE_EXTENSIONS:
            return [ext.strip() for ext in self.ALLOWED_FILE_EXTENSIONS.split(",")]
        return [".pdf", ".jpg", ".jpeg", ".png", ".docx", ".doc"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


# Initialize settings
settings = Settings()
