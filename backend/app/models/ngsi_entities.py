"""
NGSI-LD Entities Definitions
"""
from typing import Optional, List, Dict, Any
from datetime import datetime


class NGSIEntity:
    """Base NGSI-LD Entity"""
    
    def __init__(self, entity_id: str, entity_type: str):
        self.id = entity_id
        self.type = entity_type
        self.created = datetime.utcnow()
        self.modified = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "type": self.type,
            "@context": "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        }


class TouristProfile(NGSIEntity):
    """Tourist preferences and profile"""
    
    def __init__(self, tourist_id: str, name: str, language: str = "es"):
        super().__init__(tourist_id, "TouristProfile")
        self.name = name
        self.language = language
        self.nationality = None
        self.interests: List[str] = []
        self.mobility_reduced = False
        self.social_openness = "moderate"  # low, moderate, high
        self.inferred_interests: List[str] = []


class PointOfInterest(NGSIEntity):
    """Point of Interest base entity"""
    
    def __init__(self, poi_id: str, name: str, latitude: float, longitude: float):
        super().__init__(poi_id, "PointOfInterest")
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.rating = 0.0
        self.current_occupancy = 0
        self.max_capacity = 100
        self.category = "generic"


class Museum(PointOfInterest):
    """Museum entity"""
    
    def __init__(self, museum_id: str, name: str, latitude: float, longitude: float):
        super().__init__(museum_id, name, latitude, longitude)
        self.type = "Museum"
        self.price = 0.0
        self.collections: List[str] = []
        self.audio_guides: List[str] = ["es", "en", "ga"]
        self.opening_hours = "09:00-20:00"


class Beach(PointOfInterest):
    """Beach entity"""
    
    def __init__(self, beach_id: str, name: str, latitude: float, longitude: float):
        super().__init__(beach_id, name, latitude, longitude)
        self.type = "Beach"
        self.length_meters = 0.0
        self.flag_color = "green"  # green, yellow, red
        self.water_temperature = 15.0
        self.water_quality = "good"
        self.services: List[str] = []


class Event(NGSIEntity):
    """Event entity"""
    
    def __init__(self, event_id: str, name: str, location_id: str):
        super().__init__(event_id, "Event")
        self.name = name
        self.location_id = location_id
        self.event_type = "generic"  # concert, fair, route, etc
        self.start_time = datetime.utcnow()
        self.end_time = datetime.utcnow()
        self.max_capacity = 500
        self.current_occupancy = 0
        self.price = 0.0


class TouristTrip(NGSIEntity):
    """Active tourist trip/itinerary"""
    
    def __init__(self, trip_id: str, tourist_id: str, destination_id: str):
        super().__init__(trip_id, "TouristTrip")
        self.tourist_id = tourist_id
        self.destination_id = destination_id
        self.start_time = datetime.utcnow()
        self.end_time = None
        self.visited_pois: List[Dict[str, Any]] = []
        self.planned_route: List[str] = []


class SocialMatch(NGSIEntity):
    """Social connection between travelers"""
    
    def __init__(self, match_id: str, tourist_a_id: str, tourist_b_id: str):
        super().__init__(match_id, "SocialMatch")
        self.tourist_a_id = tourist_a_id
        self.tourist_b_id = tourist_b_id
        self.affinity_score = 0.0  # 0-100
        self.suggested_poi = None
        self.status = "pending"  # pending, accepted, rejected
        self.matched_at = datetime.utcnow()


class Alert(NGSIEntity):
    """Real-time alert notification"""
    
    def __init__(self, alert_id: str, alert_type: str):
        super().__init__(alert_id, "Alert")
        self.alert_type = alert_type  # occupancy, weather, event, social
        self.severity = "info"  # info, warning, critical
        self.message = ""
        self.target_entity_id = None
        self.created = datetime.utcnow()


class ConsumptionBehavior(NGSIEntity):
    """Tourist consumption and behavior data"""
    
    def __init__(self, behavior_id: str, tourist_id: str):
        super().__init__(behavior_id, "ConsumptionBehavior")
        self.tourist_id = tourist_id
        self.poi_visits: List[Dict[str, Any]] = []
        self.total_spent = 0.0
        self.total_time_minutes = 0
        self.last_updated = datetime.utcnow()


class TouristDestination(NGSIEntity):
    """Tourist destination (city)"""
    
    def __init__(self, destination_id: str, name: str, country: str):
        super().__init__(destination_id, "TouristDestination")
        self.name = name
        self.country = country
        self.season = "off-season"  # off-season, low-season, high-season
        self.supported_languages: List[str] = ["es", "en", "ga"]
        self.max_capacity = 10000
        self.current_tourists = 0


class Device(NGSIEntity):
    """IoT Device (sensor, camera, beacon)"""
    
    def __init__(self, device_id: str, device_type: str, location_id: str):
        super().__init__(device_id, "Device")
        self.device_type = device_type  # camera, beacon, sensor, etc
        self.location_id = location_id
        self.status = "active"
        self.last_reading = datetime.utcnow()
        self.reading_data: Dict[str, Any] = {}
