"""Recommendation routes"""
from fastapi import APIRouter

from app.models import ReckommendationSchema

router = APIRouter()


@router.get("/{tourist_id}/itinerary")
async def get_recommended_itinerary(tourist_id: str, num_hours: int = 4):
    """Get recommended itinerary for tourist"""
    # TODO: Call ML recommendation engine
    return {
        "tourist_id": tourist_id,
        "recommended_pois": [],
        "duration_hours": num_hours,
        "score": 0.85,
    }


@router.post("/{tourist_id}/next-stop")
async def get_next_stop(tourist_id: str, current_poi_id: str):
    """Get next recommended POI"""
    # TODO: Call ML recommendation engine
    return {
        "tourist_id": tourist_id,
        "current_poi": current_poi_id,
        "next_poi": "poi-id",
        "distance_km": 2.5,
        "estimated_time_minutes": 15,
        "affinity_score": 0.92,
    }


@router.get("/{tourist_id}/social-matches")
async def get_social_matches(tourist_id: str):
    """Get potential social matches"""
    # TODO: Call matchmaking engine
    return {
        "tourist_id": tourist_id,
        "matches": [],
    }


@router.post("/{tourist_id}/social-matches/{match_id}/accept")
async def accept_social_match(tourist_id: str, match_id: str):
    """Accept a social match"""
    # TODO: Update match status in Orion CB
    return {
        "match_id": match_id,
        "status": "accepted",
    }


@router.post("/{tourist_id}/social-matches/{match_id}/reject")
async def reject_social_match(tourist_id: str, match_id: str):
    """Reject a social match"""
    # TODO: Update match status
    return {
        "match_id": match_id,
        "status": "rejected",
    }


@router.get("/{tourist_id}/ml-model-status")
async def get_ml_status(tourist_id: str):
    """Check ML model status for tourist"""
    # TODO: Check model availability
    return {
        "tourist_id": tourist_id,
        "model_ready": True,
        "confidence": 0.88,
    }
