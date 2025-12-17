"""Application configuration"""
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Clustering Platform API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "sqlite:///./clustering_platform.db"
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    NOTEBOOK_DIR: str = "notebooks"
    TEMPLATE_DIR: str = "templates"
    VISUALIZATIONS_DIR: str = "visualizations"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: list[str] = [".csv", ".json"]
    
    # Jupyter
    JUPYTER_SERVER_URL: str = "http://localhost:8888"
    JUPYTER_TOKEN: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Encryption for device API keys
    ENCRYPTION_KEY: str = "your-encryption-key-change-in-production"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Convert to Path objects and ensure directories exist
UPLOAD_DIR = Path(settings.UPLOAD_DIR)
NOTEBOOK_DIR = Path(settings.NOTEBOOK_DIR)
TEMPLATE_DIR = Path(settings.TEMPLATE_DIR)
VISUALIZATIONS_DIR = Path(settings.VISUALIZATIONS_DIR)

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
VISUALIZATIONS_DIR.mkdir(parents=True, exist_ok=True)

# Update settings with Path objects for backward compatibility
settings.UPLOAD_DIR = UPLOAD_DIR
settings.NOTEBOOK_DIR = NOTEBOOK_DIR
settings.TEMPLATE_DIR = TEMPLATE_DIR
settings.VISUALIZATIONS_DIR = VISUALIZATIONS_DIR

