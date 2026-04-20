"""
FastAPI middleware for error handling, logging, and request/response processing.
"""

import time
import logging
from typing import Callable, Awaitable
from contextlib import asynccontextmanager

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger

# Configure loguru
logger.remove()  # Remove default handler
logger.add(
    "logs/smarttourism.log",
    rotation="500 MB",
    retention="10 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
)
logger.add(
    lambda msg: print(msg.rstrip()),  # Print to stdout
    level="INFO",
    format="{time:HH:mm:ss} | {level: <8} | {message}",
)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Global error handling middleware"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.exception(f"Unhandled exception in {request.method} {request.url.path}")
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "type": exc.__class__.__name__,
                },
            )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging incoming requests and outgoing responses"""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        # Start timer
        start_time = time.time()
        
        # Get request details
        request_id = request.headers.get("x-request-id", "none")
        method = request.method
        path = request.url.path
        client_host = request.client.host if request.client else "unknown"
        
        # Log incoming request
        logger.info(
            f"[{request_id}] {method} {path} | Client: {client_host}"
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log response with timing
            logger.info(
                f"[{request_id}] {method} {path} | Status: {response.status_code} | "
                f"Duration: {process_time:.3f}s"
            )
            
            # Add custom headers
            response.headers["x-request-id"] = request_id
            response.headers["x-process-time"] = str(process_time)
            
            return response
            
        except Exception as exc:
            process_time = time.time() - start_time
            logger.error(
                f"[{request_id}] {method} {path} | Error: {str(exc)} | "
                f"Duration: {process_time:.3f}s"
            )
            raise


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """Middleware to ensure all requests have a correlation ID"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get or generate correlation ID
        correlation_id = request.headers.get("x-correlation-id", str(int(time.time() * 1000)))
        
        # Add to request state
        request.state.correlation_id = correlation_id
        
        # Process request
        response = await call_next(request)
        
        # Add correlation ID to response
        response.headers["x-correlation-id"] = correlation_id
        
        return response


def setup_logging(log_level: str = "INFO") -> None:
    """Configure logging for the application"""
    # Remove default handler
    logger.remove()
    
    # Add file handler with rotation
    logger.add(
        "logs/smarttourism.log",
        rotation="500 MB",
        retention="10 days",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    )
    
    # Add console handler
    logger.add(
        lambda msg: print(msg.rstrip()),
        level=log_level,
        format="{time:HH:mm:ss} | {level: <8} | {message}",
    )
    
    # Set logging level for libraries
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)


def get_logger(name: str):
    """Get a logger instance with name"""
    return logger.bind(name=name)
