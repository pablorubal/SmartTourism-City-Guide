"""Tourist Profile routes"""
from fastapi import APIRouter

from app.models import TouristProfileSchema

router = APIRouter()


@router.get("/{tourist_id}", response_model=TouristProfileSchema)
async def get_tourist_profile(tourist_id: str):
    """Get tourist profile"""
    # TODO: Retrieve from Orion CB
    return {
        "id": tourist_id,
        "name": "Tourist Name",
        "nationality": "ES",
        "language": "es",
        "interests": [],
        "mobility_reduced": False,
        "social_openness": "moderate",
    }


@router.post("/", response_model=TouristProfileSchema)
async def create_tourist_profile(profile: TouristProfileSchema):
    """Create new tourist profile"""
    # TODO: Save to Orion CB
    return profile


@router.put("/{tourist_id}", response_model=TouristProfileSchema)
async def update_tourist_profile(tourist_id: str, profile: TouristProfileSchema):
    """Update tourist profile"""
    # TODO: Update in Orion CB
    return profile


@router.get("/{tourist_id}/preferences")
async def get_preferences(tourist_id: str):
    """Get tourist preferences"""
    # TODO: Retrieve preferences
    return {
        "interests": [],
        "mobility_reduced": False,
        "social_openness": "moderate",
    }


@router.post("/{tourist_id}/preferences")
async def update_preferences(tourist_id: str, preferences: dict):
    """Update tourist preferences"""
    # TODO: Save preferences to Orion CB
    return {"updated": True}
