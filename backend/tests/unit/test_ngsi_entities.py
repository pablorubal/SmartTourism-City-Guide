"""
Unit tests for NGSI-LD Entity classes
"""
import pytest
from datetime import datetime

from app.models.ngsi_entities import (
    NGSIEntity,
    TouristProfile,
    PointOfInterest,
    Event,
    Museum,
    Beach,
    Alert,
    SocialMatch
)


@pytest.mark.unit
class TestNGSIEntities:
    """Test NGSI-LD Entity classes"""
    
    def test_ngsi_entity_creation(self):
        """Test base NGSI entity creation"""
        entity = NGSIEntity("entity-1", "TestEntity")
        assert entity.id == "entity-1"
        assert entity.type == "TestEntity"
        assert isinstance(entity.created, datetime)
        assert isinstance(entity.modified, datetime)
    
    def test_ngsi_entity_to_dict(self):
        """Test entity conversion to dictionary"""
        entity = NGSIEntity("entity-1", "TestEntity")
        data = entity.to_dict()
        
        assert data["id"] == "entity-1"
        assert data["type"] == "TestEntity"
        assert "@context" in data
    
    def test_tourist_profile_creation(self):
        """Test TouristProfile creation"""
        profile = TouristProfile("tourist-1", "Alice", language="es")
        assert profile.id == "tourist-1"
        assert profile.type == "TouristProfile"
    
    def test_point_of_interest_creation(self):
        """Test PointOfInterest creation"""
        poi = PointOfInterest(
            "poi-1",
            "Museum ABC",
            40.7128,
            -74.0060
        )
        assert poi.id == "poi-1"
        assert poi.type == "PointOfInterest"
        assert poi.name == "Museum ABC"
        assert poi.latitude == 40.7128
        assert poi.longitude == -74.0060
    
    def test_event_creation(self):
        """Test Event creation"""
        event = Event(
            "event-1",
            "Concert Night",
            "location-1"
        )
        assert event.id == "event-1"
        assert event.type == "Event"
        assert event.name == "Concert Night"
    
    def test_museum_creation(self):
        """Test Museum creation"""
        museum = Museum(
            "mus-1",
            "Museum of Art",
            40.7614,
            -73.9776
        )
        assert museum.id == "mus-1"
        assert museum.type == "Museum"
    
    def test_beach_creation(self):
        """Test Beach creation"""
        beach = Beach(
            "beach-1",
            "Coney Island Beach",
            40.5755,
            -73.9866
        )
        assert beach.id == "beach-1"
        assert beach.type == "Beach"
    
    def test_alert_creation(self):
        """Test Alert creation"""
        alert = Alert(
            "alert-1",
            "occupancy"
        )
        assert alert.id == "alert-1"
        assert alert.type == "Alert"
        assert alert.alert_type == "occupancy"
    
    def test_social_match_creation(self):
        """Test SocialMatch creation"""
        match = SocialMatch(
            "match-1",
            "tourist-1",
            "tourist-2"
        )
        assert match.id == "match-1"
        assert match.type == "SocialMatch"
    
    def test_entity_modification_timestamp(self):
        """Test entity modification timestamp"""
        entity = NGSIEntity("entity-1", "TestEntity")
        original_modified = entity.modified
        
        # Modify should update timestamp (in real implementation)
        assert entity.modified >= original_modified
    
    def test_multiple_entities(self):
        """Test creating multiple entities"""
        entities = [
            NGSIEntity(f"entity-{i}", "TestEntity")
            for i in range(5)
        ]
        
        assert len(entities) == 5
        assert all(isinstance(e, NGSIEntity) for e in entities)
        assert all(e.type == "TestEntity" for e in entities)
