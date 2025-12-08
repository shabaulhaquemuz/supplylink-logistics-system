"""
Tracking Repository - GPS tracking operations
This file handles all GPS tracking database operations for driver shipments.

It acts as the repository layer so services can save and fetch tracking data without writing SQL queries.

create_tracking_entry() stores a new GPS update including latitude, longitude, location name, and status message.

Every tracking entry is timestamped automatically using datetime.utcnow().

Tracking data is stored in the shared TrackingData table defined in shared/models.py.

get_last_location() fetches the most recent location of a shipment using the latest timestamp.

This helps power live tracking, driver movement history, and customer shipment tracking screens.

In simple words — this file is the GPS tracking database helper, saving driver locations and retrieving last known positions.
"""
from sqlalchemy.orm import Session
from backend.shared.models import TrackingData
from typing import Optional
from datetime import datetime

class TrackingRepository:
    """Handle all tracking database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_tracking_entry(
        self,
        shipment_id: int,
        latitude: float,
        longitude: float,
        location_name: Optional[str] = None,
        status_update: Optional[str] = None
    ) -> TrackingData:
        """Create new tracking entry"""
        tracking = TrackingData(
            shipment_id=shipment_id,
            latitude=latitude,
            longitude=longitude,
            location_name=location_name,
            status_update=status_update,
            timestamp=datetime.utcnow()
        )
        self.db.add(tracking)
        self.db.commit()
        self.db.refresh(tracking)
        return tracking
    
    def get_last_location(self, shipment_id: int) -> Optional[TrackingData]:
        """Get last known location for shipment"""
        return self.db.query(TrackingData).filter(
            TrackingData.shipment_id == shipment_id
        ).order_by(TrackingData.timestamp.desc()).first()