"""
Unit tests for middleware
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.middleware import (
    ErrorHandlingMiddleware,
    RequestLoggingMiddleware,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestMiddleware:
    """Test middleware components"""
    
    async def test_error_handling_middleware_initialization(self):
        """Test ErrorHandlingMiddleware initialization"""
        app = MagicMock()
        middleware = ErrorHandlingMiddleware(app)
        
        assert middleware.app is not None
    
    async def test_error_handling_middleware_success(self):
        """Test middleware with successful request"""
        app = MagicMock()
        middleware = ErrorHandlingMiddleware(app)
        
        # Create mock request
        request = MagicMock(spec=Request)
        request.method = "GET"
        request.url.path = "/test"
        
        # Create mock call_next
        async def mock_call_next(req):
            return JSONResponse({"status": "ok"})
        
        response = await middleware.dispatch(request, mock_call_next)
        assert response is not None
    
    async def test_error_handling_middleware_error(self):
        """Test middleware with error handling"""
        app = MagicMock()
        middleware = ErrorHandlingMiddleware(app)
        
        request = MagicMock(spec=Request)
        request.method = "GET"
        request.url.path = "/test"
        
        # Mock call_next to raise error
        async def mock_call_next_error(req):
            raise ValueError("Test error")
        
        response = await middleware.dispatch(request, mock_call_next_error)
        assert response.status_code == 500
    
    async def test_request_logging_middleware_initialization(self):
        """Test RequestLoggingMiddleware initialization"""
        app = MagicMock()
        middleware = RequestLoggingMiddleware(app)
        
        assert middleware.app is not None
    
    async def test_request_logging_middleware_dispatch(self):
        """Test request logging middleware dispatch"""
        app = MagicMock()
        middleware = RequestLoggingMiddleware(app)
        
        request = MagicMock(spec=Request)
        request.method = "GET"
        request.url.path = "/test"
        request.headers = {}
        
        async def mock_call_next(req):
            return JSONResponse({"status": "ok"})
        
        response = await middleware.dispatch(request, mock_call_next)
        assert response is not None
