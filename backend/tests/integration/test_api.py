"""
Integration tests for API endpoints
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.integration
class TestPOIsEndpoints:
    """Test POIs API endpoints"""
    
    async def test_list_pois(self, async_client: AsyncClient):
        """Test listing POIs"""
        response = await async_client.get("/api/v1/pois")
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "total" in data
        assert "skip" in data
        assert "limit" in data
    
    async def test_list_pois_with_pagination(self, async_client: AsyncClient):
        """Test listing POIs with pagination"""
        response = await async_client.get(
            "/api/v1/pois",
            params={"skip": 0, "limit": 10}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["limit"] == 10
    
    async def test_get_poi_not_found(self, async_client: AsyncClient):
        """Test getting non-existent POI"""
        response = await async_client.get("/api/v1/pois/nonexistent-id")
        
        assert response.status_code == 404
    
    async def test_create_poi_unauthorized(self, async_client: AsyncClient, sample_poi_data):
        """Test creating POI without authentication"""
        response = await async_client.post(
            "/api/v1/pois",
            json=sample_poi_data
        )
        
        # Should be 401 or 403 without auth
        assert response.status_code in [401, 403]
    
    async def test_get_occupancy(self, async_client: AsyncClient):
        """Test getting POI occupancy"""
        response = await async_client.get(
            "/api/v1/pois/test-poi/occupancy"
        )
        
        # May be 404 if POI doesn't exist, but endpoint should be accessible
        assert response.status_code in [200, 404]
    
    async def test_update_occupancy(self, async_client: AsyncClient):
        """Test updating POI occupancy"""
        response = await async_client.post(
            "/api/v1/pois/test-poi/occupancy",
            params={"occupancy": 50}
        )
        
        # Should be 404 if POI doesn't exist
        assert response.status_code in [200, 404]


@pytest.mark.asyncio
@pytest.mark.integration
class TestTouristsEndpoints:
    """Test Tourists API endpoints"""
    
    async def test_list_tourists_not_found(self, async_client: AsyncClient):
        """Test getting tourist profile that doesn't exist"""
        response = await async_client.get(
            "/api/v1/tourists/nonexistent-user"
        )
        
        assert response.status_code == 404
    
    async def test_create_tourist_profile_missing_user(self, async_client: AsyncClient):
        """Test creating profile for non-existent user"""
        response = await async_client.post(
            "/api/v1/tourists",
            params={
                "user_id": "nonexistent-user",
                "interests": ["hiking", "museums"]
            }
        )
        
        assert response.status_code == 404
    
    async def test_get_consumption_history_empty(self, async_client: AsyncClient):
        """Test getting consumption history"""
        response = await async_client.get(
            "/api/v1/tourists/test-user/history"
        )
        
        # Should return 404 or empty list
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert "data" in data
            assert "total" in data
    
    async def test_get_recommendations(self, async_client: AsyncClient):
        """Test getting recommendations"""
        response = await async_client.get(
            "/api/v1/tourists/test-user/recommendations"
        )
        
        # Should be 404 if user doesn't exist
        assert response.status_code in [200, 404]


@pytest.mark.asyncio
@pytest.mark.integration
class TestEventsEndpoints:
    """Test Events API endpoints"""
    
    async def test_list_events(self, async_client: AsyncClient):
        """Test listing events"""
        response = await async_client.get("/api/v1/events")
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "total" in data
    
    async def test_list_events_with_pagination(self, async_client: AsyncClient):
        """Test listing events with pagination"""
        response = await async_client.get(
            "/api/v1/events",
            params={"skip": 0, "limit": 10}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["limit"] == 10
    
    async def test_get_event_not_found(self, async_client: AsyncClient):
        """Test getting non-existent event"""
        response = await async_client.get("/api/v1/events/nonexistent-id")
        
        assert response.status_code == 404
    
    async def test_get_upcoming_events(self, async_client: AsyncClient):
        """Test getting upcoming events for destination"""
        response = await async_client.get(
            "/api/v1/events/destination/coruna/upcoming"
        )
        
        # May be 404 or 200 with empty list
        assert response.status_code in [200, 404]


@pytest.mark.asyncio
@pytest.mark.integration
class TestAuthEndpoints:
    """Test authentication endpoints"""
    
    async def test_signup_success(self, async_client: AsyncClient, sample_user_data):
        """Test successful user signup"""
        response = await async_client.post(
            "/api/v1/auth/signup",
            json=sample_user_data
        )
        
        assert response.status_code in [201, 200]
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    async def test_signup_duplicate_email(self, async_client: AsyncClient, sample_user_data):
        """Test signup with duplicate email"""
        # First signup
        await async_client.post(
            "/api/v1/auth/signup",
            json=sample_user_data
        )
        
        # Try duplicate
        response = await async_client.post(
            "/api/v1/auth/signup",
            json=sample_user_data
        )
        
        assert response.status_code == 400
    
    async def test_login_invalid_email(self, async_client: AsyncClient):
        """Test login with non-existent email"""
        response = await async_client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "Password123"
            }
        )
        
        assert response.status_code == 401
    
    async def test_health_endpoint(self, async_client: AsyncClient):
        """Test health check endpoint"""
        response = await async_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    async def test_version_endpoint(self, async_client: AsyncClient):
        """Test version endpoint"""
        response = await async_client.get("/version")
        
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "app_name" in data


@pytest.mark.asyncio
@pytest.mark.integration
class TestAPIErrors:
    """Test API error handling"""
    
    async def test_404_not_found(self, async_client: AsyncClient):
        """Test 404 error response"""
        response = await async_client.get("/api/v1/nonexistent")
        
        assert response.status_code == 404
    
    async def test_invalid_query_parameters(self, async_client: AsyncClient):
        """Test invalid query parameters"""
        response = await async_client.get(
            "/api/v1/pois",
            params={"limit": "invalid"}
        )
        
        # Should be 422 (validation error)
        assert response.status_code == 422
    
    async def test_invalid_json_body(self, async_client: AsyncClient):
        """Test invalid JSON in request body"""
        response = await async_client.post(
            "/api/v1/auth/signup",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code in [400, 422]
