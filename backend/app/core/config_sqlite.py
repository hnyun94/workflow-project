from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # 기본 설정
    PROJECT_NAME: str = "비품 관리 시스템"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 데이터베이스 (SQLite for testing)
    DATABASE_URL: str = "sqlite:///./supplies.db"
    
    # 보안
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]
    
    def get_database_url(self) -> str:
        return self.DATABASE_URL
    
    class Config:
        env_file = ".env"

settings = Settings()
