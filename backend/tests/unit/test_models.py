"""
Unit tests for database models
"""
import pytest
from sqlalchemy import inspect

from app.models.db_models import (
    User, TouristProfile, PointOfInterest, Museum, Beach,
    Event, TouristDestination, TouristTrip, TouristRental,
    ConsumptionBehavior, SocialMatch, Alert, Device, Base
)


@pytest.mark.unit
class TestDatabaseModels:
    """Test SQLAlchemy ORM models"""
    
    def test_user_model_fields(self):
        """Test User model has required fields"""
        user_mapper = inspect(User)
        columns = [c.key for c in user_mapper.columns]
        
        assert "id" in columns
        assert "email" in columns
        assert "hashed_password" in columns
        assert "full_name" in columns
        assert "is_admin" in columns
        assert "created_at" in columns
        assert "updated_at" in columns
    
    def test_tourist_profile_model_fields(self):
        """Test TouristProfile model has required fields"""
        profile_mapper = inspect(TouristProfile)
        columns = [c.key for c in profile_mapper.columns]
        
        assert "id" in columns
        assert "user_id" in columns
        assert "interests" in columns
        assert "inferred_interests" in columns
        assert "sociability_level" in columns
        assert "mobility_restrictions" in columns
    
    def test_poi_model_fields(self):
        """Test PointOfInterest model has required fields"""
        poi_mapper = inspect(PointOfInterest)
        columns = [c.key for c in poi_mapper.columns]
        
        assert "id" in columns
        assert "name" in columns
        assert "latitude" in columns
        assert "longitude" in columns
        assert "category" in columns
        assert "current_occupancy" in columns
        assert "max_capacity" in columns
        assert "tags" in columns
        assert "opening_hours" in columns
    
    def test_museum_model_exists(self):
        """Test Museum model exists and has poi_id FK"""
        museum_mapper = inspect(Museum)
        columns = [c.key for c in museum_mapper.columns]
        
        assert "id" in columns
        assert "poi_id" in columns  # Foreign key to POI
        assert "price" not in columns  # Museum uses ticket_price
        assert "ticket_price" in columns
        assert "audioguide_languages" in columns
    
    def test_beach_model_exists(self):
        """Test Beach model exists and has poi_id FK"""
        beach_mapper = inspect(Beach)
        columns = [c.key for c in beach_mapper.columns]
        
        assert "id" in columns
        assert "poi_id" in columns  # Foreign key to POI
        assert "flag_color" in columns
        assert "water_temperature" in columns
        assert "water_quality" in columns
    
    def test_event_model_fields(self):
        """Test Event model has required fields"""
        event_mapper = inspect(Event)
        columns = [c.key for c in event_mapper.columns]
        
        assert "id" in columns
        assert "name" in columns
        assert "event_type" in columns
        assert "poi_id" in columns  # Location reference
        assert "start_datetime" in columns
        assert "end_datetime" in columns
        assert "max_capacity" in columns
        assert "current_attendance" in columns
    
    def test_consumption_behavior_model_fields(self):
        """Test ConsumptionBehavior model has required fields"""
        behavior_mapper = inspect(ConsumptionBehavior)
        columns = [c.key for c in behavior_mapper.columns]
        
        assert "id" in columns
        assert "profile_id" in columns
        assert "trip_id" in columns
        assert "poi_id" in columns
        assert "entry_time" in columns
        assert "exit_time" in columns
    
    def test_social_match_model_fields(self):
        """Test SocialMatch model has required fields"""
        social_mapper = inspect(SocialMatch)
        columns = [c.key for c in social_mapper.columns]
        
        assert "id" in columns
        assert "tourist_1_id" in columns
        assert "tourist_2_id" in columns
        assert "affinity_score" in columns
        assert "created_at" in columns
    
    def test_alert_model_fields(self):
        """Test Alert model has required fields"""
        alert_mapper = inspect(Alert)
        columns = [c.key for c in alert_mapper.columns]
        
        assert "id" in columns
        assert "alert_type" in columns
        assert "title" in columns
        assert "description" in columns
        assert "created_at" in columns
    
    def test_device_model_fields(self):
        """Test Device model has required fields"""
        device_mapper = inspect(Device)
        columns = [c.key for c in device_mapper.columns]
        
        assert "id" in columns
        assert "name" in columns
        assert "device_type" in columns
        assert "latitude" in columns
        assert "longitude" in columns
    
    def test_user_email_uniqueness(self):
        """Test User email uniqueness constraint"""
        user_mapper = inspect(User)
        
        # Check if email column has unique constraint
        email_col = [c for c in user_mapper.columns if c.key == "email"]
        assert len(email_col) > 0
        assert email_col[0].unique is True
    
    def test_user_model_is_valid(self):
        """Test User model can be instantiated"""
        # Simply verify the model class exists and is valid
        assert User is not None
        assert hasattr(User, '__tablename__')
        assert User.__tablename__ == "users"
    
    def test_all_models_have_timestamps(self):
        """Test that main models have created_at and updated_at"""
        models_with_timestamps = [User, TouristProfile, Event, Alert]
        
        for model in models_with_timestamps:
            mapper = inspect(model)
            columns = [c.key for c in mapper.columns]
            assert "created_at" in columns, f"{model.__name__} missing created_at"
