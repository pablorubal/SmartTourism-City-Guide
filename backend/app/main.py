"""
FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.routes import pois, tourists, events, recommendations


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    # Startup
    print("🚀 SmartTourism API starting...")
    yield
    # Shutdown
    print("🛑 SmartTourism API shutting down...")


# Create FastAPI app
app = FastAPI(
    title="SmartTourism City Guide API",
    description="Intelligent tourism guide platform for A Coruña",
    version="0.1.0",
    lifespan=lifespan,
)

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
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "SmartTourism API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
