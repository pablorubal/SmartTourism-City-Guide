"""
Points of Interest (POIs) routes
Handles CRUD operations for POIs with Orion CB integration
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.database import db_manager
from app.models.schemas import POISchema, MuseumSchema, BeachSchema
from app.models.db_models import PointOfInterest, Museum, Beach
from app.services.orion_service import OrionService
from app.websocket import ws_manager

router = APIRouter(prefix="/api/v1/pois", tags=["pois"])


@router.get("", response_model=dict)
async def list_pois(
    category: Optional[str] = Query(None, description="Filter by category"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating"),
    skip: int = Query(0, ge=0, description="Number of results to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results to return"),
):
    """
    List all Points of Interest with pagination and filters
    
    Returns POIs from database enriched with Orion CB data
    """
    try:
        async with db_manager.get_session() as session:
            # Build query
            query = select(PointOfInterest)
            
            if category:
                query = query.where(PointOfInterest.category == category)
            
            if min_rating is not None:
                # TODO: Filter by rating once rating field is available
                pass
            
            # Pagination
            result = await session.execute(
                query.offset(skip).limit(limit)
            )
            pois = result.scalars().all()
            
            # Get total count
            count_result = await session.execute(select(PointOfInterest))
            total = len(count_result.scalars().all())
            
            logger.info(f"📍 Listed {len(pois)} POIs (skip={skip}, limit={limit})")
            
            return {
                "data": [
                    {
                        "id": str(poi.id),
                        "name": poi.name,
                        "latitude": float(poi.latitude),
                        "longitude": float(poi.longitude),
                        "category": poi.category,
                        "current_occupancy": poi.occupancy_percentage or 0,
                        "max_capacity": 100,
                    }
                    for poi in pois
                ],
                "total": total,
                "skip": skip,
                "limit": limit,
            }
    
    except Exception as e:
        logger.error(f"❌ Failed to list POIs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve POIs"
        )


@router.get("/{poi_id}", response_model=dict)
async def get_poi(poi_id: str):
    """
    Get single POI with detailed information
    
    Enriched with occupancy, events, and nearby recommendations
    """
    try:
        async with db_manager.get_session() as session:
            result = await session.execute(
                select(PointOfInterest).where(PointOfInterest.id == poi_id)
            )
            poi = result.scalar_one_or_none()
            
            if not poi:
                logger.warning(f"⚠️ POI not found: {poi_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="POI not found"
                )
            
            logger.debug(f"📖 Retrieved POI: {poi.name}")
            
            return {
                "id": str(poi.id),
                "name": poi.name,
                "latitude": float(poi.latitude),
                "longitude": float(poi.longitude),
                "category": poi.category,
                "current_occupancy": poi.occupancy_percentage or 0,
                "max_capacity": 100,
                "tags": poi.tags or [],
                "created_at": poi.created_at.isoformat() if poi.created_at else None,
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get POI {poi_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve POI"
        )


@router.post("", response_model=dict, status_code=201)
async def create_poi(poi_data: POISchema):
    """
    Create new Point of Interest
    
    Creates in both database and Orion CB
    """
    try:
        async with db_manager.get_session() as session:
            # Create in database
            new_poi = PointOfInterest(
                name=poi_data.name,
                latitude=poi_data.latitude,
                longitude=poi_data.longitude,
                category=poi_data.category,
                occupancy_percentage=poi_data.current_occupancy,
                tags=[],
            )
            
            session.add(new_poi)
            await session.commit()
            await session.refresh(new_poi)
            
            # Create in Orion CB
            orion_data = {
                "name": {"type": "Property", "value": new_poi.name},
                "coordinates": {"type": "GeoProperty", "value": {"type": "Point", "coordinates": [poi_data.longitude, poi_data.latitude]}},
                "category": {"type": "Property", "value": poi_data.category},
                "occupancy": {"type": "Property", "value": poi_data.current_occupancy},
            }
            
            async with OrionService() as orion:
                await orion.create_entity(
                    entity_id=str(new_poi.id),
                    entity_type="PointOfInterest",
                    entity_data=orion_data
                )
            
            logger.info(f"✅ Created POI: {new_poi.name}")
            
            return {
                "id": str(new_poi.id),
                "name": new_poi.name,
                "latitude": float(new_poi.latitude),
                "longitude": float(new_poi.longitude),
                "category": new_poi.category,
            }
    
    except Exception as e:
        logger.error(f"❌ Failed to create POI: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create POI"
        )


@router.put("/{poi_id}", response_model=dict)
async def update_poi(poi_id: str, poi_data: POISchema):
    """
    Update existing POI
    
    Updates in both database and Orion CB
    """
    try:
        async with db_manager.get_session() as session:
            result = await session.execute(
                select(PointOfInterest).where(PointOfInterest.id == poi_id)
            )
            poi = result.scalar_one_or_none()
            
            if not poi:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="POI not found"
                )
            
            # Update in database
            poi.name = poi_data.name
            poi.latitude = poi_data.latitude
            poi.longitude = poi_data.longitude
            poi.category = poi_data.category
            poi.occupancy_percentage = poi_data.current_occupancy
            
            await session.commit()
            
            # Update in Orion CB
            orion_data = {
                "name": {"type": "Property", "value": poi_data.name},
                "occupancy": {"type": "Property", "value": poi_data.current_occupancy},
            }
            
            async with OrionService() as orion:
                await orion.update_entity(
                    entity_id=poi_id,
                    entity_type="PointOfInterest",
                    updates=orion_data
                )
            
            logger.info(f"✏️ Updated POI: {poi.name}")
            
            return {
                "id": str(poi.id),
                "name": poi.name,
                "latitude": float(poi.latitude),
                "longitude": float(poi.longitude),
                "category": poi.category,
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to update POI {poi_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update POI"
        )


@router.delete("/{poi_id}", status_code=204)
async def delete_poi(poi_id: str):
    """
    Delete Point of Interest
    
    Deletes from both database and Orion CB
    """
    try:
        async with db_manager.get_session() as session:
            result = await session.execute(
                select(PointOfInterest).where(PointOfInterest.id == poi_id)
            )
            poi = result.scalar_one_or_none()
            
            if not poi:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="POI not found"
                )
            
            # Delete from database
            await session.delete(poi)
            await session.commit()
            
            # Delete from Orion CB
            async with OrionService() as orion:
                await orion.delete_entity(
                    entity_id=poi_id,
                    entity_type="PointOfInterest"
                )
            
            logger.info(f"🗑️ Deleted POI: {poi.name}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to delete POI {poi_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete POI"
        )


@router.get("/{poi_id}/occupancy", response_model=dict)
async def get_occupancy(poi_id: str):
    """Get real-time occupancy for a POI"""
    try:
        async with db_manager.get_session() as session:
            result = await session.execute(
                select(PointOfInterest).where(PointOfInterest.id == poi_id)
            )
            poi = result.scalar_one_or_none()
            
            if not poi:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="POI not found"
                )
            
            occupancy_pct = poi.occupancy_percentage or 0
            status_flag = "green" if occupancy_pct < 70 else "yellow" if occupancy_pct < 90 else "red"
            
            return {
                "poi_id": poi_id,
                "occupancy_percentage": occupancy_pct,
                "capacity": 100,
                "status": status_flag,
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get occupancy: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve occupancy"
        )


@router.post("/{poi_id}/occupancy", response_model=dict)
async def update_occupancy(poi_id: str, occupancy: int = Query(..., ge=0, le=100)):
    """Update occupancy data (from IoT sensors)"""
    try:
        async with db_manager.get_session() as session:
            result = await session.execute(
                select(PointOfInterest).where(PointOfInterest.id == poi_id)
            )
            poi = result.scalar_one_or_none()
            
            if not poi:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="POI not found"
                )
            
            poi.occupancy_percentage = occupancy
            await session.commit()
            
            # Broadcast update via WebSocket
            await ws_manager.broadcast_to_channel(
                channel="poi_occupancy",
                message_type="occupancy_update",
                data={
                    "poi_id": poi_id,
                    "occupancy": occupancy,
                    "status": "green" if occupancy < 70 else "yellow" if occupancy < 90 else "red",
                }
            )
            
            logger.info(f"📊 Updated occupancy for {poi.name}: {occupancy}%")
            
            return {
                "poi_id": poi_id,
                "occupancy": occupancy,
                "updated": True
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to update occupancy: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update occupancy"
        )
