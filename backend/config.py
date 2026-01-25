from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    # Database Configuration
    # Default to SQLite for development (change to PostgreSQL for production)
    # Use an absolute path so running uvicorn from any folder still finds the same DB file.
    DATABASE_URL: str = f"sqlite:///{(Path(__file__).resolve().parent / 'uni_arena.db').as_posix()}"
    
    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS Configuration
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Application Configuration
    PROJECT_NAME: str = "Uni Arena"
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
