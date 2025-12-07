"""Application configuration."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Base configuration."""
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://flask_user:flask_password@localhost:5432/flask_app')
    
    # Connection Pool Settings
    DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', 10))
    DB_MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', 20))
    DB_POOL_TIMEOUT = int(os.getenv('DB_POOL_TIMEOUT', 30))
    DB_POOL_RECYCLE = int(os.getenv('DB_POOL_RECYCLE', 3600))
    
    # SSL Configuration
    DB_SSL_MODE = os.getenv('DB_SSL_MODE', 'prefer')
    
    # Application Settings
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')
    TESTING = False
    
    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    # Use SQLite in-memory database for testing (no PostgreSQL required)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # Disable connection pooling for tests
    DB_POOL_SIZE = 1
    DB_MAX_OVERFLOW = 0
    # SQLite doesn't use SSL
    DB_SSL_MODE = None


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # In production, ensure SSL is properly configured
    DB_SSL_MODE = os.getenv('DB_SSL_MODE', 'require')


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
