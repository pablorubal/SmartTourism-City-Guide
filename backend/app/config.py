"""
Application Configuration
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # App
    APP_NAME: str = "SmartTourism City Guide"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # API
    API_V1_STR: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173", "*"]
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/smartourism"
    
    # Orion Context Broker
    ORION_URL: str = "http://localhost:1026"
    ORION_TENANT: str = "smartourism"
    ORION_VERSION: str = "v2"
    
    # QuantumLeap
    QUANTUMLEAP_URL: str = "http://localhost:8668"
    
    # Redis (for caching & WebSockets)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # ML Models
    MODEL_PATH: str = "/models"
    ENABLE_ML: bool = True
    
    # Ollama (Local LLM)
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    
    # A Coruña coordinates (default destination)
    DEFAULT_LAT: float = 43.3622
    DEFAULT_LON: float = -8.3886
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Load settings
settings = Settings()
