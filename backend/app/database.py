"""
Database configuration and session management for SmartTourism.
Uses SQLAlchemy with asyncpg for async database access to TimescaleDB.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# Create declarative base for all models
class Base(DeclarativeBase):
    """Base class for all database models"""
    pass


class DatabaseManager:
    """Manages database connections and sessions"""

    def __init__(self):
        self.engine = None
        self.async_session = None

    def initialize(self):
        """Initialize database engine and session factory"""
        # Create async engine with asyncpg dialect
        self.engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            pool_pre_ping=True,
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_max_overflow,
            # Use NullPool for development to avoid connection issues
            poolclass=NullPool if settings.debug else None,
        )

        # Create async session factory
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

    async def create_all_tables(self):
        """Create all database tables from models"""
        if self.engine is None:
            self.initialize()

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all_tables(self):
        """Drop all database tables (for testing/reset)"""
        if self.engine is None:
            self.initialize()

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get a new async session.
        Usage as dependency in FastAPI routes.
        """
        if self.async_session is None:
            self.initialize()

        async with self.async_session() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def close(self):
        """Close database connections"""
        if self.engine:
            await self.engine.dispose()


# Global database manager instance
db_manager = DatabaseManager()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for FastAPI routes to inject session"""
    async for session in db_manager.get_session():
        yield session


async def init_db():
    """Initialize database (create tables)"""
    db_manager.initialize()
    await db_manager.create_all_tables()


async def close_db():
    """Close database connections"""
    await db_manager.close()
