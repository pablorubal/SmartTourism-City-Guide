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
    ENVIRONMENT: str = "development"
    
    # API
    API_V1_STR: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173", "http://localhost"]
    
    # Database Configuration
    DATABASE_URL: str = "postgresql+asyncpg://smarttourism:smarttourism_dev@localhost:5432/smarttourism_db"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 40
    DB_ECHO_SQL: bool = False
    
    # Orion Context Broker (NGSI-LD)
    ORION_URL: str = "http://localhost:1026"
    ORION_TENANT: str = "smarttourism"
    ORION_VERSION: str = "ld"
    ORION_TIMEOUT: int = 10
    
    # QuantumLeap (Time Series Data)
    QUANTUMLEAP_URL: str = "http://localhost:8668"
    
    # Redis (Caching & WebSockets)
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_TTL: int = 3600
    
    # ML Models
    MODEL_PATH: str = "/models"
    ENABLE_ML: bool = True
    
    # Ollama (Local LLM for Chat)
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    OLLAMA_TIMEOUT: int = 60
    
    # JWT Configuration
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # A Coruña coordinates (default destination)
    DEFAULT_DESTINATION_LAT: float = 43.3622
    DEFAULT_DESTINATION_LON: float = -8.3886
    DEFAULT_DESTINATION_NAME: str = "A Coruña"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Features
    ENABLE_SWAGGER: bool = True
    ENABLE_PROFILING: bool = False
    ENABLE_MOCK_DATA: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Load settings
settings = Settings()

