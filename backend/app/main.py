"""
FastAPI Application Entry Point
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config import settings
from app.database import init_db, close_db, db_manager
from app.middleware import (
    setup_logging,
    ErrorHandlingMiddleware,
    RequestLoggingMiddleware,
    CorrelationIDMiddleware,
)
from app.routes import pois, tourists, events, recommendations


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    # Startup
    logger.info("🚀 SmartTourism API starting...")
    
    # Initialize logging
    setup_logging(settings.LOG_LEVEL)
    
    # Initialize database
    logger.info("📊 Initializing database...")
    try:
        await init_db()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 SmartTourism API shutting down...")
    await close_db()
    logger.info("✅ Database connections closed")


# Create FastAPI app
app = FastAPI(
    title="SmartTourism City Guide API",
    description="Intelligent tourism guide platform for A Coruña with NGSI-LD integration",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.ENABLE_SWAGGER else None,
    openapi_url="/openapi.json" if settings.ENABLE_SWAGGER else None,
)

# Add middleware (order matters - first added = last executed)
app.add_middleware(CorrelationIDMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
app.include_router(pois.router, prefix="/api/v1/pois", tags=["POIs"])
app.include_router(tourists.router, prefix="/api/v1/tourists", tags=["Tourists"])
app.include_router(events.router, prefix="/api/v1/events", tags=["Events"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["Recommendations"])


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint"""
    return {
        "message": "🗺️ SmartTourism City Guide API",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "running",
        "docs": "/docs" if settings.ENABLE_SWAGGER else None,
    }


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SmartTourism API",
        "database": "connected",
        "orion": settings.ORION_URL,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/version", tags=["Health"])
async def version():
    """Get API version"""
    return {
        "version": settings.APP_VERSION,
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.DEBUG)
