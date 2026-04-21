"""
Events routes
Handles event management and listings
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select
from loguru import logger

from app.database import db_manager
from app.models.db_models import Event
from app.models.schemas import EventSchema
from app.services.orion_service import OrionService
from app.websocket import ws_manager

router = APIRouter(prefix="/api/v1/events", tags=["events"])


@router.get("", response_model=dict)
async def list_events(
    destination_id: Optional[str] = Query(None, description="Filter by destination"),
    upcoming_only: bool = Query(True, description="Show only upcoming events"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    """
    List all events with pagination
    
    Args:
        destination_id: Optional destination ID to filter by
        upcoming_only: Only return future events
        skip: Pagination offset
        limit: Pagination limit
    """
    try:
        async with db_manager.session_context() as session:
            query = select(Event)
            
            if upcoming_only:
                query = query.where(Event.end_datetime > datetime.utcnow())
            
            if destination_id:
                query = query.where(Event.location_id == destination_id)
            
            # Get total count
            count_result = await session.execute(query)
            total = len(count_result.scalars().all())
            
            # Get paginated results
            result = await session.execute(
                query.offset(skip).limit(limit)
            )
            events = result.scalars().all()
            
            logger.info(f"📅 Listed {len(events)} events (skip={skip}, limit={limit})")
            
            return {
                "data": [
                    {
                        "id": str(event.id),
                        "name": event.name,
                        "event_type": event.event_type,
                        "location_id": str(event.location_id),
                        "start_time": event.start_datetime.isoformat() if event.start_datetime else None,
                        "end_time": event.end_datetime.isoformat() if event.end_datetime else None,
                        "max_capacity": event.max_capacity or 500,
                        "current_occupancy": event.current_attendance or 0,
                    }
                    for event in events
                ],
                "total": total,
                "skip": skip,
                "limit": limit,
            }
    
    except Exception as e:
        logger.error(f"❌ Failed to list events: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve events"
        )


@router.get("/{event_id}", response_model=dict)
async def get_event(event_id: str):
    """Get event details"""
    try:
        async with db_manager.session_context() as session:
            result = await session.execute(
                select(Event).where(Event.id == event_id)
            )
            event = result.scalar_one_or_none()
            
            if not event:
                logger.warning(f"⚠️ Event not found: {event_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Event not found"
                )
            
            logger.debug(f"📖 Retrieved event: {event.name}")
            
            return {
                "id": str(event.id),
                "name": event.name,
                "event_type": event.event_type,
                "location_id": str(event.location_id),
                "start_time": event.start_datetime.isoformat() if event.start_datetime else None,
                "end_time": event.end_datetime.isoformat() if event.end_datetime else None,
                "max_capacity": event.max_capacity or 500,
                "current_occupancy": event.current_attendance or 0,
                "description": getattr(event, 'description', None),
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get event {event_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve event"
        )


@router.post("", response_model=dict, status_code=201)
async def create_event(event_data: EventSchema):
    """Create new event (admin only)"""
    try:
        async with db_manager.session_context() as session:
            # Create in database
            new_event = Event(
                name=event_data.name,
                event_type=event_data.event_type,
                location_id=event_data.location_id,
                start_datetime=event_data.start_time,
                end_datetime=event_data.end_time,
                max_capacity=event_data.max_capacity,
                current_attendance=0,
            )
            
            session.add(new_event)
            await session.commit()
            await session.refresh(new_event)
            
            # Create in Orion CB
            orion_data = {
                "name": {"type": "Property", "value": new_event.name},
                "eventType": {"type": "Property", "value": event_data.event_type},
                "startDateTime": {"type": "Property", "value": new_event.start_datetime.isoformat()},
                "endDateTime": {"type": "Property", "value": new_event.end_datetime.isoformat()},
                "maxCapacity": {"type": "Property", "value": new_event.max_capacity},
            }
            
            async with OrionService() as orion:
                await orion.create_entity(
                    entity_id=str(new_event.id),
                    entity_type="Event",
                    entity_data=orion_data
                )
            
            logger.info(f"✅ Created event: {new_event.name}")
            
            return {
                "id": str(new_event.id),
                "name": new_event.name,
                "event_type": new_event.event_type,
            }
    
    except Exception as e:
        logger.error(f"❌ Failed to create event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create event"
        )


@router.put("/{event_id}", response_model=dict)
async def update_event(event_id: str, event_data: EventSchema):
    """Update event (admin only)"""
    try:
        async with db_manager.session_context() as session:
            result = await session.execute(
                select(Event).where(Event.id == event_id)
            )
            event = result.scalar_one_or_none()
            
            if not event:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Event not found"
                )
            
            # Update in database
            event.name = event_data.name
            event.event_type = event_data.event_type
            event.start_datetime = event_data.start_time
            event.end_datetime = event_data.end_time
            event.max_capacity = event_data.max_capacity
            
            await session.commit()
            
            # Update in Orion CB
            orion_data = {
                "name": {"type": "Property", "value": event_data.name},
                "maxCapacity": {"type": "Property", "value": event_data.max_capacity},
            }
            
            async with OrionService() as orion:
                await orion.update_entity(
                    entity_id=event_id,
                    entity_type="Event",
                    updates=orion_data
                )
            
            logger.info(f"✏️ Updated event: {event.name}")
            
            return {
                "id": str(event.id),
                "name": event.name,
                "event_type": event.event_type,
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to update event {event_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update event"
        )


@router.get("/{event_id}/occupancy", response_model=dict)
async def get_event_occupancy(event_id: str):
    """Get event occupancy status"""
    try:
        async with db_manager.session_context() as session:
            result = await session.execute(
                select(Event).where(Event.id == event_id)
            )
            event = result.scalar_one_or_none()
            
            if not event:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Event not found"
                )
            
            occupancy_pct = (event.current_attendance / event.max_capacity * 100) if event.max_capacity else 0
            status_flag = "green" if occupancy_pct < 70 else "yellow" if occupancy_pct < 90 else "red"
            
            return {
                "event_id": event_id,
                "occupancy_percentage": round(occupancy_pct, 2),
                "current_attendance": event.current_attendance or 0,
                "max_capacity": event.max_capacity,
                "status": status_flag,
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get event occupancy: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve occupancy"
        )


@router.get("/destination/{destination_id}/upcoming", response_model=dict)
async def get_upcoming_events(destination_id: str, days_ahead: int = Query(7, ge=1, le=30)):
    """Get upcoming events for a destination"""
    try:
        async with db_manager.session_context() as session:
            from sqlalchemy import and_
            
            result = await session.execute(
                select(Event).where(
                    and_(
                        Event.location_id == destination_id,
                        Event.end_datetime > datetime.utcnow(),
                    )
                ).limit(20)
            )
            events = result.scalars().all()
            
            logger.info(f"📅 Found {len(events)} upcoming events for {destination_id}")
            
            return {
                "destination_id": destination_id,
                "events": [
                    {
                        "id": str(event.id),
                        "name": event.name,
                        "start_time": event.start_datetime.isoformat() if event.start_datetime else None,
                        "occupancy_pct": (event.current_attendance / event.max_capacity * 100) if event.max_capacity else 0,
                    }
                    for event in events
                ],
                "total": len(events),
            }
    
    except Exception as e:
        logger.error(f"❌ Failed to get upcoming events: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve events"
        )
