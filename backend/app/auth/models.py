"""
Authentication models and schemas
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class TokenRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "tourist@example.com",
                "password": "SecurePassword123"
            }
        }


class TokenResponse(BaseModel):
    """JWT token response schema"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # Seconds until expiration
    user_id: str = None
    email: str = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 86400,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "tourist@example.com"
            }
        }


class SignupRequest(BaseModel):
    """User registration request schema"""
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    full_name: str = Field(min_length=2, max_length=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "tourist@example.com",
                "password": "SecurePassword123",
                "full_name": "John Doe"
            }
        }


class UserAuth(BaseModel):
    """User authentication data"""
    user_id: str
    email: str
    is_admin: bool = False
    exp: int = None  # Token expiration timestamp
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "tourist@example.com",
                "is_admin": False,
                "exp": 1640000000
            }
        }


class RefreshTokenRequest(BaseModel):
    """Token refresh request"""
    refresh_token: str


class LogoutRequest(BaseModel):
    """Logout request"""
    token: Optional[str] = None
