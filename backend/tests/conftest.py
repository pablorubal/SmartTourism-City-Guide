"""
Global pytest configuration and fixtures
"""
import sys
import os

import asyncio
from typing import Generator, AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

# Lazy imports - these will be resolved when fixtures are called
app = None
db_manager = None
Base = None

def _ensure_imports():
    """Lazy import app modules"""
    global app, db_manager, Base
    if app is None:
        from app.main import app as app_instance
        from app.database import db_manager as db_mgr
        from app.models.db_models import Base as BaseModel
        app = app_instance
        db_manager = db_mgr
        Base = BaseModel


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Create in-memory SQLite database for testing
    
    Uses:
    - In-memory SQLite (:memory:)
    - StaticPool for test isolation
    - Auto-creates/drops tables
    """
    _ensure_imports()
    from sqlalchemy.ext.asyncio import async_sessionmaker
    
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        poolclass=StaticPool,
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session factory
    async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    
    # Yield session for tests
    async with async_session_maker() as session:
        yield session
    
    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Create async HTTP client for testing API endpoints
    
    Uses TestClient from httpx to test FastAPI routes
    """
    _ensure_imports()
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_orion_response():
    """Mock successful Orion CB response"""
    return {
        "@context": "https://www.w3.org/2022/wot/td/v1.1",
        "id": "urn:ngsi-ld:PointOfInterest:test-poi",
        "type": "PointOfInterest",
        "name": {"type": "Property", "value": "Test POI"},
        "coordinates": {
            "type": "GeoProperty",
            "value": {"type": "Point", "coordinates": [-8.3886, 43.3622]}
        },
    }


@pytest.fixture
def mock_jwt_token():
    """Mock valid JWT token"""
    from app.auth.jwt import create_access_token
    return create_access_token(
        data={
            "sub": "550e8400-e29b-41d4-a716-446655440000",
            "email": "test@example.com",
            "is_admin": False,
        }
    )


@pytest.fixture
def mock_admin_token():
    """Mock admin JWT token"""
    from app.auth.jwt import create_access_token
    return create_access_token(
        data={
            "sub": "admin-user-id",
            "email": "admin@example.com",
            "is_admin": True,
        }
    )


@pytest.fixture
def sample_poi_data():
    """Sample POI data for testing"""
    return {
        "name": "Torre de Hércules",
        "latitude": 43.3869,
        "longitude": -8.3891,
        "category": "monument",
        "current_occupancy": 45,
        "max_capacity": 200,
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "email": "tourist@example.com",
        "password": "TestPassword123",
        "full_name": "Test Tourist",
    }


@pytest.fixture
def sample_event_data():
    """Sample event data for testing"""
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    return {
        "name": "Test Concert",
        "event_type": "concert",
        "location_id": "location-1",
        "start_time": (now + timedelta(days=1)).isoformat(),
        "end_time": (now + timedelta(days=1, hours=3)).isoformat(),
        "max_capacity": 500,
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    # Setup Python path early so modules can be imported
    sys.path = [p for p in sys.path if p != '/']
    if '/app' not in sys.path:
        sys.path.insert(0, '/app')
    
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
