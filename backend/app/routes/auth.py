"""
Authentication routes
"""
from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from loguru import logger

from app.database import db_manager
from app.auth.jwt import create_access_token, verify_token
from app.auth.models import TokenRequest, TokenResponse, SignupRequest, UserAuth
from app.models.db_models import User
from app.config import settings


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/login", response_model=TokenResponse, status_code=200)
async def login(request: TokenRequest) -> TokenResponse:
    """
    User login endpoint
    
    Returns JWT access token on successful authentication
    """
    async with db_manager.get_session() as session:
        # Find user by email
        result = await session.execute(
            select(User).where(User.email == request.email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            logger.warning(f"❌ Login failed: User not found - {request.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Verify password
        if not verify_password(request.password, user.hashed_password):
            logger.warning(f"❌ Login failed: Invalid password - {request.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Create token
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "is_admin": user.is_admin
        }
        
        access_token = create_access_token(token_data)
        
        logger.info(f"✅ Login successful: {user.email}")
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.JWT_EXPIRATION_HOURS * 3600,
            user_id=str(user.id),
            email=user.email
        )


@router.post("/signup", response_model=TokenResponse, status_code=201)
async def signup(request: SignupRequest) -> TokenResponse:
    """
    User registration endpoint
    
    Creates new user and returns JWT access token
    """
    async with db_manager.get_session() as session:
        # Check if user already exists
        result = await session.execute(
            select(User).where(User.email == request.email)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            logger.warning(f"❌ Signup failed: Email already registered - {request.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        new_user = User(
            email=request.email,
            hashed_password=hash_password(request.password),
            is_admin=False
        )
        
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        
        logger.info(f"✅ Signup successful: {new_user.email}")
        
        # Create token
        token_data = {
            "sub": str(new_user.id),
            "email": new_user.email,
            "is_admin": False
        }
        
        access_token = create_access_token(token_data)
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.JWT_EXPIRATION_HOURS * 3600,
            user_id=str(new_user.id),
            email=new_user.email
        )


@router.post("/refresh", response_model=TokenResponse, status_code=200)
async def refresh_token(current_token: str) -> TokenResponse:
    """
    Refresh JWT token
    
    Returns new token with extended expiration
    """
    # Verify current token (even if expired, we'll accept it for refresh)
    payload = verify_token(current_token)
    
    if not payload:
        logger.warning("❌ Token refresh failed: Invalid or expired token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Create new token with same data
    token_data = {
        "sub": payload.get("sub"),
        "email": payload.get("email"),
        "is_admin": payload.get("is_admin", False)
    }
    
    access_token = create_access_token(token_data)
    
    logger.info(f"✅ Token refreshed for: {payload.get('email')}")
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.JWT_EXPIRATION_HOURS * 3600,
        user_id=payload.get("sub"),
        email=payload.get("email")
    )


@router.post("/logout", status_code=204)
async def logout():
    """
    Logout endpoint
    
    In a real application, you would add the token to a blacklist.
    For now, this is a placeholder.
    
    Frontend should delete the token from localStorage/sessionStorage.
    """
    logger.info("✅ Logout successful")
    return None


async def get_current_user(token: str) -> UserAuth:
    """
    Dependency to get current authenticated user from token
    
    Usage in routes:
        @router.get("/protected")
        async def protected_route(current_user: UserAuth = Depends(get_current_user)):
            ...
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token provided"
        )
    
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return UserAuth(
        user_id=payload.get("sub"),
        email=payload.get("email"),
        is_admin=payload.get("is_admin", False),
        exp=payload.get("exp")
    )
