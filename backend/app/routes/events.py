"""Events routes"""
from fastapi import APIRouter
from typing import List

from app.models import EventSchema

router = APIRouter()


@router.get("/", response_model=List[EventSchema])
async def list_events(destination_id: str = None):
    """List all events"""
    # TODO: Retrieve events from Orion CB
    return []


@router.get("/{event_id}", response_model=EventSchema)
async def get_event(event_id: str):
    """Get event details"""
    # TODO: Retrieve from Orion CB
    return {
        "id": event_id,
        "name": "Event Name",
        "location_id": "location-1",
        "event_type": "concert",
        "start_time": "2026-04-15T20:00:00",
        "end_time": "2026-04-15T23:00:00",
        "max_capacity": 500,
        "current_occupancy": 250,
        "price": 25.0,
    }


@router.post("/", response_model=EventSchema)
async def create_event(event: EventSchema):
    """Create new event"""
    # TODO: Save to Orion CB
    return event


@router.get("/{event_id}/occupancy")
async def get_event_occupancy(event_id: str):
    """Get event occupancy"""
    # TODO: Retrieve occupancy data
    return {
        "event_id": event_id,
        "occupancy_percentage": 50,
        "capacity": 500,
    }


@router.get("/{destination_id}/upcoming")
async def get_upcoming_events(destination_id: str):
    """Get upcoming events for a destination"""
    # TODO: Retrieve upcoming events from Orion CB
    return []
