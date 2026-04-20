"""POIs routes"""
from fastapi import APIRouter, HTTPException
from typing import List

from app.models import POISchema, MuseumSchema, BeachSchema

router = APIRouter()


@router.get("/", response_model=List[POISchema])
async def list_pois(
    category: str = None,
    lat: float = None,
    lon: float = None,
    radius_km: float = 5.0,
):
    """List all Points of Interest, optionally filtered"""
    # TODO: Implement POI listing with Orion CB
    return [
        {
            "id": "torre-hercules",
            "name": "Torre de Hércules",
            "latitude": 43.3869,
            "longitude": -8.3891,
            "rating": 4.5,
            "current_occupancy": 45,
            "max_capacity": 200,
            "category": "monument",
        }
    ]


@router.get("/{poi_id}", response_model=POISchema)
async def get_poi(poi_id: str):
    """Get specific POI details"""
    # TODO: Implement POI retrieval from Orion CB
    return {
        "id": poi_id,
        "name": "Example POI",
        "latitude": 43.3622,
        "longitude": -8.3886,
        "rating": 4.0,
        "current_occupancy": 50,
        "max_capacity": 100,
        "category": "museum",
    }


@router.get("/{poi_id}/occupancy")
async def get_occupancy(poi_id: str):
    """Get real-time occupancy for a POI"""
    # TODO: Connect to occupancy sensors/devices
    return {
        "poi_id": poi_id,
        "occupancy_percentage": 45,
        "capacity": 200,
        "status": "green",  # green, yellow, red
    }


@router.post("/{poi_id}/occupancy")
async def update_occupancy(poi_id: str, occupancy: int):
    """Update occupancy data (from IoT sensors)"""
    # TODO: Validate and update occupancy in Orion CB
    return {"poi_id": poi_id, "occupancy": occupancy, "updated": True}


@router.get("/museums", response_model=List[MuseumSchema])
async def list_museums():
    """List all museums"""
    # TODO: Implement museum listing
    return []


@router.get("/beaches", response_model=List[BeachSchema])
async def list_beaches():
    """List all beaches"""
    # TODO: Implement beach listing
    return []
