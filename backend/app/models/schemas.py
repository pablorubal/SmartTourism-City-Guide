"""
Pydantic Schemas for Request/Response validation
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class POISchema(BaseModel):
    """Point of Interest Schema"""
    id: str
    name: str
    latitude: float
    longitude: float
    rating: float = Field(0.0, ge=0, le=5)
    current_occupancy: int = 0
    max_capacity: int = 100
    category: str = "generic"
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "torre-hercules",
                "name": "Torre de Hércules",
                "latitude": 43.3869,
                "longitude": -8.3891,
                "rating": 4.5,
                "current_occupancy": 45,
                "max_capacity": 200,
                "category": "monument"
            }
        }


class MuseumSchema(POISchema):
    """Museum Schema"""
    price: float = 0.0
    collections: List[str] = []
    audio_guides: List[str] = ["es", "en"]
    opening_hours: str = "09:00-20:00"


class BeachSchema(POISchema):
    """Beach Schema"""
    length_meters: float = 0.0
    flag_color: str = "green"
    water_temperature: float = 15.0
    water_quality: str = "good"
    services: List[str] = []


class EventSchema(BaseModel):
    """Event Schema"""
    id: str
    name: str
    location_id: str
    event_type: str
    start_time: datetime
    end_time: datetime
    max_capacity: int = 500
    current_occupancy: int = 0
    price: float = 0.0


class TouristProfileSchema(BaseModel):
    """Tourist Profile Schema"""
    id: str
    name: str
    nationality: Optional[str] = None
    language: str = "es"
    interests: List[str] = []
    mobility_reduced: bool = False
    social_openness: str = "moderate"
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "tourist-123",
                "name": "María García",
                "nationality": "ES",
                "language": "es",
                "interests": ["architecture", "museums", "food"],
                "mobility_reduced": False,
                "social_openness": "high"
            }
        }


class TouristTripSchema(BaseModel):
    """Tourist Trip Schema"""
    id: str
    tourist_id: str
    destination_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    visited_pois: List[dict] = []
    planned_route: List[str] = []


class RecommendationSchema(BaseModel):
    """Recommendation Schema"""
    tourist_id: str
    recommended_pois: List[POISchema]
    score: float = Field(0.0, ge=0, le=1)
    rationale: str = ""


class SocialMatchSchema(BaseModel):
    """Social Match Schema"""
    match_id: str
    tourist_a_id: str
    tourist_b_id: str
    affinity_score: float = Field(0.0, ge=0, le=100)
    suggested_poi: Optional[str] = None
    status: str = "pending"
    matched_at: datetime


class AlertSchema(BaseModel):
    """Alert Schema"""
    id: str
    alert_type: str
    severity: str = "info"
    message: str
    target_entity_id: Optional[str] = None
    created: datetime


class HealthSchema(BaseModel):
    """Health Check Schema"""
    status: str
    service: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
