"""
Tourist Profile routes
Handles tourist profile management and history
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select
from loguru import logger

from app.database import db_manager
from app.models.db_models import TouristProfile, User, ConsumptionBehavior
from app.auth.jwt import TokenManager
from app.config import settings

router = APIRouter(prefix="/api/v1/tourists", tags=["tourists"])


@router.get("/{tourist_id}", response_model=dict)
async def get_tourist_profile(tourist_id: str, token: Optional[str] = None):
    """
    Get tourist profile with consumption history and recommendations
    
    Args:
        tourist_id: Tourist ID (user ID)
        token: Optional JWT token for authorization
    """
    try:
        async with db_manager.get_session() as session:
            # Check authorization
            if token:
                user_data = TokenManager.get_user_from_token(token)
                if not user_data or (user_data["user_id"] != tourist_id and not user_data.get("is_admin")):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not authorized"
                    )
            
            # Get tourist profile
            result = await session.execute(
                select(TouristProfile).where(TouristProfile.user_id == tourist_id)
            )
            profile = result.scalar_one_or_none()
            
            if not profile:
                logger.warning(f"⚠️ Tourist profile not found: {tourist_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tourist profile not found"
                )
            
            logger.debug(f"📖 Retrieved profile for tourist: {tourist_id}")
            
            return {
                "user_id": str(profile.user_id),
                "interests": profile.interests or [],
                "inferred_interests": profile.inferred_interests or [],
                "sociability_level": profile.sociability_level or "neutral",
                "mobility_restrictions": profile.mobility_restrictions,
                "created_at": profile.created_at.isoformat() if profile.created_at else None,
                "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve profile"
        )


@router.post("", response_model=dict, status_code=201)
async def create_tourist_profile(
    user_id: str = Query(..., description="User ID"),
    interests: List[str] = Query(None, description="List of interests"),
    sociability_level: str = Query("neutral", regex="^(quiet|neutral|social)$"),
):
    """
    Create new tourist profile
    
    Typically called after user signup
    """
    try:
        async with db_manager.get_session() as session:
            # Check if user exists
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Check if profile already exists
            result = await session.execute(
                select(TouristProfile).where(TouristProfile.user_id == user_id)
            )
            if result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Profile already exists"
                )
            
            # Create profile
            profile = TouristProfile(
                user_id=user_id,
                interests=interests or [],
                sociability_level=sociability_level,
                mobility_restrictions=False,
            )
            
            session.add(profile)
            await session.commit()
            await session.refresh(profile)
            
            logger.info(f"✅ Created profile for tourist: {user_id}")
            
            return {
                "user_id": str(profile.user_id),
                "interests": profile.interests,
                "sociability_level": profile.sociability_level,
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to create profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create profile"
        )


@router.put("/{tourist_id}", response_model=dict)
async def update_tourist_profile(
    tourist_id: str,
    interests: Optional[List[str]] = Query(None),
    sociability_level: Optional[str] = Query(None, regex="^(quiet|neutral|social)$"),
    mobility_restrictions: Optional[bool] = Query(None),
):
    """Update tourist preferences and settings"""
    try:
        async with db_manager.get_session() as session:
            result = await session.execute(
                select(TouristProfile).where(TouristProfile.user_id == tourist_id)
            )
            profile = result.scalar_one_or_none()
            
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tourist profile not found"
                )
            
            # Update fields if provided
            if interests is not None:
                profile.interests = interests
            if sociability_level is not None:
                profile.sociability_level = sociability_level
            if mobility_restrictions is not None:
                profile.mobility_restrictions = mobility_restrictions
            
            await session.commit()
            await session.refresh(profile)
            
            logger.info(f"✏️ Updated profile for tourist: {tourist_id}")
            
            return {
                "user_id": str(profile.user_id),
                "interests": profile.interests,
                "sociability_level": profile.sociability_level,
                "mobility_restrictions": profile.mobility_restrictions,
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to update profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )


@router.get("/{tourist_id}/history", response_model=dict)
async def get_consumption_history(
    tourist_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    """
    Get tourist consumption history (visited POIs, spending)
    
    Paginated list of consumption behavior records
    """
    try:
        async with db_manager.get_session() as session:
            # Get total count
            count_result = await session.execute(
                select(ConsumptionBehavior).where(
                    ConsumptionBehavior.tourist_id == tourist_id
                )
            )
            total = len(count_result.scalars().all())
            
            # Get paginated results
            result = await session.execute(
                select(ConsumptionBehavior)
                .where(ConsumptionBehavior.tourist_id == tourist_id)
                .offset(skip)
                .limit(limit)
            )
            records = result.scalars().all()
            
            logger.debug(f"📊 Retrieved {len(records)} consumption records for {tourist_id}")
            
            return {
                "data": [
                    {
                        "poi_id": str(record.poi_id),
                        "entry_time": record.entry_time.isoformat() if record.entry_time else None,
                        "exit_time": record.exit_time.isoformat() if record.exit_time else None,
                        "duration_minutes": record.duration_minutes,
                        "amount_spent": float(record.amount_spent) if record.amount_spent else 0,
                        "interest_category": record.interest_category,
                    }
                    for record in records
                ],
                "total": total,
                "skip": skip,
                "limit": limit,
            }
    
    except Exception as e:
        logger.error(f"❌ Failed to get consumption history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve history"
        )


@router.get("/{tourist_id}/recommendations", response_model=dict)
async def get_recommendations(tourist_id: str):
    """
    Get ML-based POI recommendations for tourist
    
    Returns personalized recommendations based on:
    - Interests
    - Consumption history
    - Social matching
    - Current location/time
    """
    try:
        async with db_manager.get_session() as session:
            # Get tourist profile
            result = await session.execute(
                select(TouristProfile).where(TouristProfile.user_id == tourist_id)
            )
            profile = result.scalar_one_or_none()
            
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tourist profile not found"
                )
            
            # TODO: Implement actual ML recommendation engine
            # For now, return placeholder recommendations
            logger.info(f"💡 Generated recommendations for {tourist_id}")
            
            return {
                "tourist_id": tourist_id,
                "recommendations": [
                    {
                        "poi_id": "poi-1",
                        "name": "Recommended POI",
                        "reason": "Matches your interests",
                        "score": 0.92,
                    }
                ],
                "strategy": "ML-based",
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get recommendations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate recommendations"
        )
