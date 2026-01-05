"""
Application Settings - WITH SUPABASE SUPPORT
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings
    
    Environment variables from .env file
    """
    
    # ========================================
    # API Configuration
    # ========================================
    PROJECT_NAME: str = "End.STP"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    
    # ========================================
    # Database
    # ========================================
    DATABASE_URL: str = "postgresql://postgres:your_password@localhost:5432/endstp"
    
    # ========================================
    # Supabase (NEW)
    # ========================================
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    SUPABASE_JWT_SECRET: str = ""
    
    # ========================================
    # Security
    # ========================================
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # ========================================
    # CORS
    # ========================================
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # ========================================
    # Logging
    # ========================================
    LOG_LEVEL: str = "INFO"
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # CRITICAL: Ignore extra .env fields


settings = Settings()