"""
Orion Context Broker Integration Service
Handles CRUD operations with retry logic and error handling
"""
from typing import Optional, Dict, Any, List, Callable
from datetime import datetime
import httpx
from loguru import logger
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from app.clients.orion_client import OrionClient
from app.config import settings


class OrionService:
    """Service for Orion Context Broker operations with resilience"""
    
    def __init__(self):
        """Initialize Orion service"""
        self.client: Optional[OrionClient] = None
        self.base_endpoint = "/ngsi-ld/v1/entities"
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.client = OrionClient()
        await self.client.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, Exception)),
        reraise=True
    )
    async def create_entity(
        self,
        entity_id: str,
        entity_type: str,
        entity_data: Dict[str, Any],
        service_path: str = "/"
    ) -> Dict[str, Any]:
        """
        Create NGSI-LD entity in Orion CB
        
        Args:
            entity_id: Entity ID
            entity_type: NGSI-LD entity type
            entity_data: Entity attributes and properties
            service_path: Fiware-ServicePath
            
        Returns:
            Created entity data
            
        Raises:
            httpx.HTTPError: If creation fails after retries
        """
        try:
            entity = {
                "@context": [
                    "https://www.w3.org/2022/wot/td/v1.1"
                ],
                "id": f"urn:ngsi-ld:{entity_type}:{entity_id}",
                "type": entity_type,
                **entity_data
            }
            
            response = await self.client.post(
                self.base_endpoint,
                entity,
                service_path=service_path
            )
            
            logger.info(f"✅ Created entity: {entity_type}:{entity_id}")
            return entity
        
        except httpx.HTTPError as e:
            logger.error(f"❌ Failed to create entity {entity_id}: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, Exception)),
        reraise=True
    )
    async def get_entity(
        self,
        entity_id: str,
        entity_type: str = None,
        service_path: str = "/"
    ) -> Dict[str, Any]:
        """
        Retrieve NGSI-LD entity from Orion CB
        
        Args:
            entity_id: Entity ID
            entity_type: Optional entity type filter
            service_path: Fiware-ServicePath
            
        Returns:
            Entity data
            
        Raises:
            httpx.HTTPStatusError: If entity not found or error occurs
        """
        try:
            entity_urn = f"urn:ngsi-ld:{entity_type}:{entity_id}" if entity_type else entity_id
            endpoint = f"{self.base_endpoint}/{entity_urn}"
            
            response = await self.client.get(
                endpoint,
                service_path=service_path
            )
            
            entity = response.json()
            logger.debug(f"📖 Retrieved entity: {entity_id}")
            return entity
        
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.warning(f"⚠️ Entity not found: {entity_id}")
            else:
                logger.error(f"❌ Failed to get entity {entity_id}: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, Exception)),
        reraise=True
    )
    async def update_entity(
        self,
        entity_id: str,
        entity_type: str,
        updates: Dict[str, Any],
        service_path: str = "/"
    ) -> Dict[str, Any]:
        """
        Update NGSI-LD entity in Orion CB
        
        Args:
            entity_id: Entity ID
            entity_type: Entity type
            updates: Attributes to update
            service_path: Fiware-ServicePath
            
        Returns:
            Updated entity data
            
        Raises:
            httpx.HTTPError: If update fails after retries
        """
        try:
            entity_urn = f"urn:ngsi-ld:{entity_type}:{entity_id}"
            endpoint = f"{self.base_endpoint}/{entity_urn}/attrs"
            
            response = await self.client.patch(
                endpoint,
                updates,
                service_path=service_path
            )
            
            logger.info(f"✏️ Updated entity: {entity_type}:{entity_id}")
            
            # Retrieve updated entity
            return await self.get_entity(entity_id, entity_type, service_path)
        
        except httpx.HTTPError as e:
            logger.error(f"❌ Failed to update entity {entity_id}: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, Exception)),
        reraise=True
    )
    async def delete_entity(
        self,
        entity_id: str,
        entity_type: str,
        service_path: str = "/"
    ) -> bool:
        """
        Delete NGSI-LD entity from Orion CB
        
        Args:
            entity_id: Entity ID
            entity_type: Entity type
            service_path: Fiware-ServicePath
            
        Returns:
            True if deleted successfully
            
        Raises:
            httpx.HTTPError: If deletion fails after retries
        """
        try:
            entity_urn = f"urn:ngsi-ld:{entity_type}:{entity_id}"
            endpoint = f"{self.base_endpoint}/{entity_urn}"
            
            response = await self.client.delete(
                endpoint,
                service_path=service_path
            )
            
            logger.info(f"🗑️ Deleted entity: {entity_type}:{entity_id}")
            return True
        
        except httpx.HTTPError as e:
            logger.error(f"❌ Failed to delete entity {entity_id}: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, Exception)),
        reraise=True
    )
    async def query_entities(
        self,
        entity_type: str,
        filters: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 20,
        service_path: str = "/"
    ) -> Dict[str, Any]:
        """
        Query NGSI-LD entities from Orion CB with pagination
        
        Args:
            entity_type: Entity type to query
            filters: Query filters (e.g., {"category": "museum"})
            skip: Number of results to skip (pagination)
            limit: Maximum results to return
            service_path: Fiware-ServicePath
            
        Returns:
            Dictionary with "data" (list of entities) and "total" (count)
            
        Raises:
            httpx.HTTPError: If query fails after retries
        """
        try:
            # Build query string
            params = {
                "type": entity_type,
                "limit": min(limit, 1000),  # Orion max
                "offset": skip,
            }
            
            # Add filters if provided
            if filters:
                filter_str = " and ".join([
                    f"{k}=={v}" if isinstance(v, str) else f"{k}=={v}"
                    for k, v in filters.items()
                ])
                params["q"] = filter_str
            
            response = await self.client.get(
                self.base_endpoint,
                params=params,
                service_path=service_path
            )
            
            entities = await response.json()
            total = int(response.headers.get("Fiware-ResultCount", len(entities)))
            
            logger.debug(f"🔍 Query {entity_type}: found {len(entities)} entities")
            
            return {
                "data": entities,
                "total": total,
                "skip": skip,
                "limit": limit
            }
        
        except httpx.HTTPError as e:
            logger.error(f"❌ Failed to query {entity_type}: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, Exception)),
        reraise=True
    )
    async def subscribe_to_changes(
        self,
        entity_type: str,
        callback_url: str,
        description: str = "SmartTourism Subscription",
        service_path: str = "/"
    ) -> Dict[str, Any]:
        """
        Subscribe to entity changes in Orion CB
        
        Args:
            entity_type: Entity type to subscribe to
            callback_url: URL to POST notifications to
            description: Subscription description
            service_path: Fiware-ServicePath
            
        Returns:
            Subscription data with subscription ID
            
        Raises:
            httpx.HTTPError: If subscription fails after retries
        """
        try:
            subscription = {
                "@context": "https://www.w3.org/2022/wot/td/v1.1",
                "type": "Subscription",
                "entities": [{"type": entity_type}],
                "notification": {
                    "endpoint": {
                        "uri": callback_url,
                        "accept": "application/ld+json"
                    }
                },
                "description": description
            }
            
            response = await self.client.post(
                "/ngsi-ld/v1/subscriptions",
                subscription,
                service_path=service_path
            )
            
            # Extract subscription ID from location header
            location = response.headers.get("Location", "")
            sub_id = location.split("/")[-1] if location else "unknown"
            
            logger.info(f"📬 Created subscription for {entity_type}: {sub_id}")
            
            return {
                "subscription_id": sub_id,
                "entity_type": entity_type,
                "callback_url": callback_url
            }
        
        except httpx.HTTPError as e:
            logger.error(f"❌ Failed to subscribe to {entity_type}: {str(e)}")
            raise


# Global service instance
_orion_service: Optional[OrionService] = None


async def get_orion_service() -> OrionService:
    """Get Orion CB service instance"""
    global _orion_service
    if not _orion_service:
        _orion_service = OrionService()
    return _orion_service
