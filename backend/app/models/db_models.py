"""
SQLAlchemy ORM models for SmartTourism entities.
These models map to the 12 NGSI-LD entity types.
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    Text,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid

from app.database import Base


class User(Base):
    """User account for tourists and administrators"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = relationship("TouristProfile", back_populates="user", uselist=False)
    trips = relationship("TouristTrip", back_populates="user")


class TouristProfile(Base):
    """Profile of a tourist - NGSI-LD TouristProfile"""
    __tablename__ = "tourist_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Basic info
    preferred_language = Column(String(10), default="es")
    nationality = Column(String(100), nullable=True)
    birth_year = Column(Integer, nullable=True)
    
    # Interests and preferences
    interests = Column(JSON, default=list)  # Array of interest tags
    mobility_restrictions = Column(String(255), nullable=True)
    sociability_level = Column(String(50), default="medium")  # low, medium, high
    
    # Inferred attributes (updated by ML)
    inferred_interests = Column(JSON, default=dict)  # ML-discovered interests
    interest_confidence = Column(JSON, default=dict)  # Confidence scores
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="profile")
    consumption_behaviors = relationship("ConsumptionBehavior", back_populates="profile")
    social_matches = relationship("SocialMatch", back_populates="tourist_1")


class TouristTrip(Base):
    """Active itinerary - NGSI-LD TouristTrip"""
    __tablename__ = "tourist_trips"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    destination_id = Column(UUID(as_uuid=True), ForeignKey("tourist_destinations.id"), nullable=False)
    
    # Trip details
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Planned vs actual
    planned_pois = Column(JSON, default=list)  # Array of POI IDs
    visited_pois = Column(JSON, default=list)  # With timestamps
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="trips")
    destination = relationship("TouristDestination", back_populates="trips")
    consumption_behaviors = relationship("ConsumptionBehavior", back_populates="trip")


class TouristDestination(Base):
    """City/destination - NGSI-LD TouristDestination"""
    __tablename__ = "tourist_destinations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    
    # Geographic info
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Destination info
    supported_languages = Column(ARRAY(String), default=list)
    average_rating = Column(Float, default=0.0)
    max_tourist_capacity = Column(Integer, nullable=True)
    current_tourist_count = Column(Integer, default=0)
    
    # Season/timing
    peak_season_months = Column(ARRAY(Integer), default=list)
    weather = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    trips = relationship("TouristTrip", back_populates="destination")
    pois = relationship("PointOfInterest", back_populates="destination")


class PointOfInterest(Base):
    """Point of Interest - NGSI-LD PointOfInterest"""
    __tablename__ = "points_of_interest"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(UUID(as_uuid=True), ForeignKey("tourist_destinations.id"), nullable=False)
    
    # Basic info
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)  # museum, beach, restaurant, etc
    
    # Location
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String(500), nullable=True)
    
    # Ratings and reviews
    average_rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    
    # Occupancy
    max_capacity = Column(Integer, nullable=True)
    current_occupancy = Column(Integer, default=0)
    occupancy_percentage = Column(Float, default=0.0)
    
    # Metadata
    tags = Column(ARRAY(String), default=list)
    opening_hours = Column(JSON, nullable=True)
    contact = Column(JSON, nullable=True)  # phone, email, website
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    destination = relationship("TouristDestination", back_populates="pois")
    museums = relationship("Museum", back_populates="poi", uselist=False)
    beaches = relationship("Beach", back_populates="poi", uselist=False)


class Museum(Base):
    """Museum - NGSI-LD Museum (extends POI)"""
    __tablename__ = "museums"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    poi_id = Column(UUID(as_uuid=True), ForeignKey("points_of_interest.id"), nullable=False)
    
    # Museum-specific info
    max_capacity = Column(Integer, nullable=True)
    ticket_price = Column(Float, nullable=True)
    collections = Column(JSON, default=list)  # Array of collection names
    
    # Audioguide languages
    audioguide_languages = Column(ARRAY(String), default=list)
    
    # Hours
    opening_hours = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    poi = relationship("PointOfInterest", back_populates="museums")


class Beach(Base):
    """Beach - NGSI-LD Beach (extends POI)"""
    __tablename__ = "beaches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    poi_id = Column(UUID(as_uuid=True), ForeignKey("points_of_interest.id"), nullable=False)
    
    # Beach-specific info
    length_meters = Column(Float, nullable=True)
    
    # Safety/conditions
    flag_color = Column(String(20), default="green")  # green, yellow, red
    water_temperature = Column(Float, nullable=True)
    water_quality = Column(String(100), nullable=True)
    
    # Services
    services = Column(JSON, default=list)  # lifeguards, showers, rentals, etc
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    poi = relationship("PointOfInterest", back_populates="beaches")


class Event(Base):
    """Event (concert, festival, tour) - NGSI-LD Event"""
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic info
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    event_type = Column(String(100), nullable=False)  # concert, festival, tour, etc
    
    # Location - can be at POI or custom coordinates
    poi_id = Column(UUID(as_uuid=True), ForeignKey("points_of_interest.id"), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Timing
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=True)
    
    # Occupancy and pricing
    max_capacity = Column(Integer, nullable=True)
    current_attendance = Column(Integer, default=0)
    ticket_price = Column(Float, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_cancelled = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TouristRental(Base):
    """Rental service (bikes, scooters, tours) - NGSI-LD TouristRental"""
    __tablename__ = "tourist_rentals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Service info
    name = Column(String(255), nullable=False)
    service_type = Column(String(100), nullable=False)  # bike, scooter, tour, etc
    description = Column(Text, nullable=True)
    
    # Location
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Availability
    total_items = Column(Integer, nullable=True)
    available_items = Column(Integer, nullable=True)
    
    # Pricing
    hourly_price = Column(Float, nullable=True)
    daily_price = Column(Float, nullable=True)
    
    # Contact
    phone = Column(String(20), nullable=True)
    website = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ConsumptionBehavior(Base):
    """Consumption behavior tracking - NGSI-LD ConsumptionBehavior"""
    __tablename__ = "consumption_behaviors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("tourist_profiles.id"), nullable=False)
    trip_id = Column(UUID(as_uuid=True), ForeignKey("tourist_trips.id"), nullable=True)
    
    # Behavior tracking
    poi_id = Column(String(255), nullable=True)  # Reference to NGSI-LD POI
    entry_time = Column(DateTime, nullable=False)
    exit_time = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    
    # Spending
    amount_spent = Column(Float, default=0.0)
    currency = Column(String(3), default="EUR")
    
    # Inferred data
    interest_category = Column(String(100), nullable=True)
    engagement_level = Column(String(50), nullable=True)  # low, medium, high
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    profile = relationship("TouristProfile", back_populates="consumption_behaviors")
    trip = relationship("TouristTrip", back_populates="consumption_behaviors")


class SocialMatch(Base):
    """Social connection between tourists - NGSI-LD SocialMatch"""
    __tablename__ = "social_matches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    tourist_1_id = Column(UUID(as_uuid=True), ForeignKey("tourist_profiles.id"), nullable=False)
    tourist_2_id = Column(UUID(as_uuid=True), ForeignKey("tourist_profiles.id"), nullable=False)
    
    # Matching metrics
    affinity_score = Column(Float, default=0.0)  # 0.0 to 1.0
    common_interests = Column(JSON, default=list)
    
    # Meeting suggestion
    suggested_poi_id = Column(String(255), nullable=True)
    suggested_time = Column(DateTime, nullable=True)
    
    # Status
    status = Column(String(50), default="pending")  # pending, accepted, rejected, met
    
    # Timestamps
    suggested_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    tourist_1 = relationship("TouristProfile", foreign_keys=[tourist_1_id], back_populates="social_matches")


class Alert(Base):
    """Alert notification - NGSI-LD Alert"""
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Alert info
    alert_type = Column(String(100), nullable=False)  # occupancy, weather, event, social_match
    severity = Column(String(50), default="info")  # info, warning, critical
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Target
    destination_id = Column(UUID(as_uuid=True), ForeignKey("tourist_destinations.id"), nullable=True)
    poi_id = Column(String(255), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Data
    data = Column(JSON, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_read = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)


class Device(Base):
    """IoT Device - NGSI-LD Device"""
    __tablename__ = "devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Device info
    name = Column(String(255), nullable=False)
    device_type = Column(String(100), nullable=False)  # camera, beacon, sensor, qr_code
    
    # Location
    location_poi_id = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    last_heartbeat = Column(DateTime, nullable=True)
    
    # Device-specific config
    configuration = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
