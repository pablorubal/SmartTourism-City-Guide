"""
Unit tests for Orion Client
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from app.clients.orion_client import OrionClient


@pytest.mark.unit
@pytest.mark.asyncio
class TestOrionClient:
    """Test Orion Context Broker HTTP client"""
    
    def test_client_initialization(self):
        """Test OrionClient initialization"""
        client = OrionClient(base_url="http://localhost:1026", tenant="smarttourism")
        assert client.base_url == "http://localhost:1026"
        assert client.tenant == "smarttourism"
    
    async def test_client_context_manager(self):
        """Test OrionClient as context manager"""
        async with OrionClient(base_url="http://localhost:1026") as client:
            assert client is not None
            assert client.client is not None
    
    async def test_get_headers(self):
        """Test header generation"""
        client = OrionClient(base_url="http://localhost:1026", tenant="smarttourism")
        headers = client._get_headers(service_path="/api")
        
        assert headers["Fiware-Service"] == "smarttourism"
        assert headers["Fiware-ServicePath"] == "/api"
        assert "Content-Type" in headers
    
    async def test_get_request_success(self):
        """Test successful GET request"""
        with patch("httpx.AsyncClient.get") as mock_get:
            response = MagicMock()
            response.status_code = 200
            response.raise_for_status = MagicMock()
            mock_get.return_value = response
            
            async with OrionClient(base_url="http://localhost:1026") as client:
                result = await client.get("/ngsi-ld/v1/entities", params={"type": "PointOfInterest"})
                assert result is not None
                mock_get.assert_called_once()
    
    async def test_post_request_success(self):
        """Test successful POST request"""
        with patch("httpx.AsyncClient.post") as mock_post:
            response = MagicMock()
            response.status_code = 201
            response.raise_for_status = MagicMock()
            mock_post.return_value = response
            
            async with OrionClient(base_url="http://localhost:1026") as client:
                result = await client.post(
                    "/ngsi-ld/v1/entities",
                    data={"type": "PointOfInterest", "id": "poi-1"}
                )
                assert result is not None
                mock_post.assert_called_once()
    
    async def test_patch_request_success(self):
        """Test successful PATCH request"""
        with patch("httpx.AsyncClient.patch") as mock_patch:
            response = MagicMock()
            response.status_code = 204
            response.raise_for_status = MagicMock()
            mock_patch.return_value = response
            
            async with OrionClient(base_url="http://localhost:1026") as client:
                result = await client.patch(
                    "/ngsi-ld/v1/entities/entity-1",
                    data={"name": {"value": "Updated"}}
                )
                assert result is not None
                mock_patch.assert_called_once()
    
    async def test_delete_request_success(self):
        """Test successful DELETE request"""
        with patch("httpx.AsyncClient.delete") as mock_delete:
            response = MagicMock()
            response.status_code = 204
            response.raise_for_status = MagicMock()
            mock_delete.return_value = response
            
            async with OrionClient(base_url="http://localhost:1026") as client:
                result = await client.delete("/ngsi-ld/v1/entities/entity-1")
                assert result is not None
                mock_delete.assert_called_once()
    
    async def test_request_headers_included(self):
        """Test that requests include proper headers"""
        with patch("httpx.AsyncClient.get") as mock_get:
            response = MagicMock()
            response.raise_for_status = MagicMock()
            mock_get.return_value = response
            
            async with OrionClient(base_url="http://localhost:1026", tenant="smarttourism") as client:
                await client.get("/ngsi-ld/v1/entities")
                
                # Check headers were passed
                call_kwargs = mock_get.call_args[1]
                assert "headers" in call_kwargs
                headers = call_kwargs["headers"]
                assert headers["Fiware-Service"] == "smarttourism"
