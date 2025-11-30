"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

# Get the backend directory path
BACKEND_DIR = Path(__file__).parent.parent

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str
    DB_NAME: str = "logistics_db"
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_URL: str = "redis://localhost:6379"
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT_USER: int = 8001
    API_PORT_DRIVER: int = 8002
    API_PORT_ADMIN: int = 8003
    
    # External APIs
    GOOGLE_MAPS_API_KEY: Optional[str] = None
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    
    class Config:
        env_file = str(BACKEND_DIR / ".env")
        env_file_encoding = 'utf-8'
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env

settings = Settings()