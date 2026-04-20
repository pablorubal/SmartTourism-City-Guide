"""
JWT Token handling for authentication
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from loguru import logger

from app.config import settings


class TokenManager:
    """Manages JWT token creation and verification"""
    
    @staticmethod
    def create_access_token(
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create JWT access token
        
        Args:
            data: Token payload (user_id, email, etc.)
            expires_delta: Token expiration time
            
        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        logger.debug(f"🎫 Created token for: {data.get('sub', 'unknown')}")
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode JWT token
        
        Args:
            token: JWT token to verify
            
        Returns:
            Decoded token payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        
        except jwt.ExpiredSignatureError:
            logger.warning("⏰ Token expired")
            return None
        
        except jwt.InvalidTokenError as e:
            logger.warning(f"❌ Invalid token: {str(e)}")
            return None
    
    @staticmethod
    def get_user_from_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Extract user information from token
        
        Args:
            token: JWT token
            
        Returns:
            User data dictionary or None if invalid
        """
        payload = TokenManager.verify_token(token)
        
        if not payload:
            return None
        
        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "is_admin": payload.get("is_admin", False),
            "exp": payload.get("exp")
        }


# Helper functions for convenience
def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT token"""
    return TokenManager.create_access_token(data, expires_delta)


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify JWT token"""
    return TokenManager.verify_token(token)


def get_user_from_token(token: str) -> Optional[Dict[str, Any]]:
    """Get user from token"""
    return TokenManager.get_user_from_token(token)
