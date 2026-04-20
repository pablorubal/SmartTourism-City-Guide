"""
Unit tests for database configuration and management
"""
import pytest

from app.database import db_manager
from app.config import settings


@pytest.mark.unit
class TestDatabase:
    """Test database setup and management"""
    
    def test_settings_database_url(self):
        """Test database URL from settings"""
        assert settings.DATABASE_URL is not None
        assert "sqlite" in settings.DATABASE_URL or "postgresql" in settings.DATABASE_URL
    
    def test_db_manager_initialization(self):
        """Test database manager initialization"""
        assert db_manager is not None


