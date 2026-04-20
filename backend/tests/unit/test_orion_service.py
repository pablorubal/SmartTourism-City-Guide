"""
Unit tests for Orion Context Broker integration
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import Response
import json

from app.services.orion_service import OrionService


@pytest.mark.asyncio
@pytest.mark.unit
class TestOrionService:
    """Test Orion CB service operations"""
    
    @pytest.mark.asyncio
    async def test_create_entity_success(self, mock_orion_response):
        """Test successful entity creation"""
        with patch("app.services.orion_service.OrionClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value = mock_instance
            
            # Mock the post method
            response = AsyncMock()
            response.json.return_value = mock_orion_response
            mock_instance.post.return_value = response
            
            async with OrionService() as service:
                service.client = mock_instance
                
                result = await service.create_entity(
                    entity_id="test-poi",
                    entity_type="PointOfInterest",
                    entity_data={
                        "name": {"type": "Property", "value": "Test POI"}
                    }
                )
            
            assert result is not None
            mock_instance.post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_entity_success(self, mock_orion_response):
        """Test successful entity retrieval"""
        with patch("app.services.orion_service.OrionClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value = mock_instance
            
            response = AsyncMock()
            response.json.return_value = mock_orion_response
            mock_instance.get.return_value = response
            
            async with OrionService() as service:
                service.client = mock_instance
                
                result = await service.get_entity(
                    entity_id="test-poi",
                    entity_type="PointOfInterest"
                )
            
            assert result is not None
            mock_instance.get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_entity_not_found(self):
        """Test entity not found error"""
        from httpx import HTTPStatusError
        
        with patch("app.services.orion_service.OrionClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value = mock_instance
            
            # Mock 404 response
            response = MagicMock()
            response.status_code = 404
            error = HTTPStatusError("Not found", request=MagicMock(), response=response)
            mock_instance.get.side_effect = error
            
            async with OrionService() as service:
                service.client = mock_instance
                
                with pytest.raises(HTTPStatusError):
                    await service.get_entity(
                        entity_id="nonexistent",
                        entity_type="PointOfInterest"
                    )
    
    @pytest.mark.asyncio
    async def test_update_entity_success(self, mock_orion_response):
        """Test successful entity update"""
        with patch("app.services.orion_service.OrionClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value = mock_instance
            
            response = AsyncMock()
            response.json.return_value = mock_orion_response
            mock_instance.patch.return_value = response
            mock_instance.get.return_value = response
            
            async with OrionService() as service:
                service.client = mock_instance
                
                result = await service.update_entity(
                    entity_id="test-poi",
                    entity_type="PointOfInterest",
                    updates={"name": {"type": "Property", "value": "Updated POI"}}
                )
            
            assert result is not None
            mock_instance.patch.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_delete_entity_success(self):
        """Test successful entity deletion"""
        with patch("app.services.orion_service.OrionClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value = mock_instance
            
            response = AsyncMock()
            mock_instance.delete.return_value = response
            
            async with OrionService() as service:
                service.client = mock_instance
                
                result = await service.delete_entity(
                    entity_id="test-poi",
                    entity_type="PointOfInterest"
                )
            
            assert result is True
            mock_instance.delete.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_query_entities_success(self):
        """Test successful entity query"""
        with patch("app.services.orion_service.OrionClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value = mock_instance
            
            # Create a proper async mock response
            response = MagicMock()
            response.json = AsyncMock(return_value=[
                {
                    "id": "urn:ngsi-ld:PointOfInterest:poi-1",
                    "type": "PointOfInterest",
                    "name": {"type": "Property", "value": "POI 1"}
                }
            ])
            response.headers = {"Fiware-ResultCount": "1"}
            mock_instance.get = AsyncMock(return_value=response)
            
            async with OrionService() as service:
                service.client = mock_instance
                
                result = await service.query_entities(
                    entity_type="PointOfInterest",
                    filters={"category": "museum"},
                    skip=0,
                    limit=20
                )
            
            assert result["total"] == 1
            assert len(result["data"]) == 1
            mock_instance.get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_retry_logic_on_failure(self):
        """Test retry logic when request fails"""
        from httpx import ConnectError
        
        with patch("app.services.orion_service.OrionClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value = mock_instance
            
            # Fail all attempts
            mock_instance.get.side_effect = ConnectError("Connection failed")
            
            async with OrionService() as service:
                service.client = mock_instance
                
                # Should retry 3 times then raise
                with pytest.raises(ConnectError):
                    await service.get_entity(
                        entity_id="test",
                        entity_type="PointOfInterest"
                    )
