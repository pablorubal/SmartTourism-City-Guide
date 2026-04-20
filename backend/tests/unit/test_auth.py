"""
Unit tests for JWT authentication
"""
import pytest
from datetime import datetime, timedelta
import jwt

from app.auth.jwt import TokenManager, create_access_token, verify_token, get_user_from_token
from app.config import settings


@pytest.mark.unit
class TestTokenManager:
    """Test JWT token operations"""
    
    def test_create_access_token_success(self):
        """Test successful token creation"""
        data = {
            "sub": "user-123",
            "email": "test@example.com",
            "is_admin": False
        }
        
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_access_token_with_custom_expiration(self):
        """Test token creation with custom expiration"""
        data = {"sub": "user-123"}
        custom_delta = timedelta(hours=1)
        
        token = create_access_token(data, expires_delta=custom_delta)
        
        # Decode to check expiration
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        assert "exp" in payload
    
    def test_verify_token_success(self):
        """Test successful token verification"""
        data = {
            "sub": "user-123",
            "email": "test@example.com"
        }
        
        token = create_access_token(data)
        payload = verify_token(token)
        
        assert payload is not None
        assert payload["sub"] == "user-123"
        assert payload["email"] == "test@example.com"
    
    def test_verify_token_invalid(self):
        """Test verification of invalid token"""
        invalid_token = "invalid.token.here"
        
        payload = verify_token(invalid_token)
        
        assert payload is None
    
    def test_verify_token_expired(self):
        """Test verification of expired token"""
        data = {"sub": "user-123"}
        
        # Create token with past expiration
        expired_delta = timedelta(seconds=-1)
        token = create_access_token(data, expires_delta=expired_delta)
        
        payload = verify_token(token)
        
        assert payload is None
    
    def test_get_user_from_token_success(self):
        """Test user extraction from token"""
        data = {
            "sub": "user-123",
            "email": "test@example.com",
            "is_admin": False
        }
        
        token = create_access_token(data)
        user = get_user_from_token(token)
        
        assert user is not None
        assert user["user_id"] == "user-123"
        assert user["email"] == "test@example.com"
        assert user["is_admin"] is False
    
    def test_get_user_from_invalid_token(self):
        """Test user extraction from invalid token"""
        user = get_user_from_token("invalid.token.here")
        
        assert user is None
    
    def test_token_payload_integrity(self):
        """Test that token payload cannot be tampered with"""
        data = {
            "sub": "user-123",
            "email": "test@example.com"
        }
        
        token = create_access_token(data)
        
        # Try to modify token
        parts = token.split(".")
        modified_token = f"{parts[0]}.{parts[1]}.invalid_signature"
        
        payload = verify_token(modified_token)
        
        assert payload is None  # Should fail verification
    
    def test_token_algorithm_hs256(self):
        """Test that HS256 algorithm is used"""
        data = {"sub": "user-123"}
        
        token = create_access_token(data)
        
        # Decode header
        header = jwt.get_unverified_header(token)
        
        assert header["alg"] == "HS256"


@pytest.mark.asyncio
@pytest.mark.unit
class TestAuthenticationIntegration:
    """Test authentication flow integration"""
    
    async def test_login_flow(self, async_client, sample_user_data):
        """Test complete login flow"""
        # First create user via signup
        signup_response = await async_client.post(
            "/api/v1/auth/signup",
            json=sample_user_data
        )
        
        if signup_response.status_code in [200, 201]:
            signup_data = signup_response.json()
            
            # Then login with same credentials
            login_response = await async_client.post(
                "/api/v1/auth/login",
                json={
                    "email": sample_user_data["email"],
                    "password": sample_user_data["password"]
                }
            )
            
            assert login_response.status_code in [200, 201]
            assert "access_token" in login_response.json()
            assert login_response.json()["token_type"] == "bearer"
