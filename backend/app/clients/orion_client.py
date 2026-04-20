"""
HTTP Client wrapper for Orion Context Broker (NGSI-LD)
"""
from typing import Optional, Dict, Any, List
import httpx
from loguru import logger

from app.config import settings


class OrionClient:
    """Low-level HTTP client for Orion Context Broker communication"""
    
    def __init__(self, base_url: str = None, tenant: str = None, timeout: int = None):
        """
        Initialize Orion client
        
        Args:
            base_url: Orion CB base URL (default from settings)
            tenant: Fiware-Service tenant name
            timeout: Request timeout in seconds
        """
        self.base_url = (base_url or settings.ORION_URL).rstrip("/")
        self.tenant = tenant or settings.ORION_TENANT
        self.timeout = timeout or settings.ORION_TIMEOUT
        self.client = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.client = httpx.AsyncClient(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.client:
            await self.client.aclose()
    
    def _get_headers(self, service_path: str = "/") -> Dict[str, str]:
        """
        Get standard Orion CB headers
        
        Args:
            service_path: Fiware-ServicePath header value
            
        Returns:
            Dictionary of headers
        """
        return {
            "Fiware-Service": self.tenant,
            "Fiware-ServicePath": service_path,
            "Content-Type": "application/ld+json",
        }
    
    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        service_path: str = "/"
    ) -> httpx.Response:
        """
        Make GET request to Orion CB
        
        Args:
            endpoint: API endpoint (e.g., "/ngsi-ld/v1/entities")
            params: Query parameters
            service_path: Fiware-ServicePath
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(service_path)
        
        logger.debug(f"🔵 GET {endpoint} | tenant={self.tenant}")
        response = await self.client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response
    
    async def post(
        self,
        endpoint: str,
        data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
        service_path: str = "/"
    ) -> httpx.Response:
        """
        Make POST request to Orion CB
        
        Args:
            endpoint: API endpoint
            data: Request body (NGSI-LD entity)
            params: Query parameters
            service_path: Fiware-ServicePath
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(service_path)
        
        logger.debug(f"🟢 POST {endpoint} | tenant={self.tenant}")
        response = await self.client.post(
            url,
            json=data,
            params=params,
            headers=headers
        )
        response.raise_for_status()
        return response
    
    async def patch(
        self,
        endpoint: str,
        data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
        service_path: str = "/"
    ) -> httpx.Response:
        """
        Make PATCH request to Orion CB
        
        Args:
            endpoint: API endpoint
            data: Request body (entity attributes)
            params: Query parameters
            service_path: Fiware-ServicePath
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(service_path)
        
        logger.debug(f"🟡 PATCH {endpoint} | tenant={self.tenant}")
        response = await self.client.patch(
            url,
            json=data,
            params=params,
            headers=headers
        )
        response.raise_for_status()
        return response
    
    async def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        service_path: str = "/"
    ) -> httpx.Response:
        """
        Make DELETE request to Orion CB
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            service_path: Fiware-ServicePath
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(service_path)
        
        logger.debug(f"🔴 DELETE {endpoint} | tenant={self.tenant}")
        response = await self.client.delete(url, params=params, headers=headers)
        response.raise_for_status()
        return response


# Global client instance
_orion_client: Optional[OrionClient] = None


async def get_orion_client() -> OrionClient:
    """Get Orion CB client instance"""
    global _orion_client
    if not _orion_client:
        _orion_client = OrionClient()
    return _orion_client
