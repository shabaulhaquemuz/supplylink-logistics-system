"""
Driver Service - Business logic for driver operations
This file contains the business logic layer for all driver-related features in the backend.

It uses three repositories (driver, shipment, tracking) to interact with the database cleanly.

authenticate_driver() checks driver credentials, verifies account status, and generates a JWT token.

It ensures that only active and valid drivers can log in.

get_dashboard_data() collects real-time metrics like completed deliveries, pending tasks and failures.

The method also fetches the driver’s last known location from tracking data to show in their dashboard.

update_location() saves GPS updates and associates them with a shipment when applicable.

In simple terms — this service is the brain of the driver backend, managing all rules and logic before updating or reading from the database.
"""
from sqlalchemy.orm import Session
from backend.driver_backend.repositories.driver_repository import DriverRepository
from backend.driver_backend.repositories.shipment_repository import ShipmentRepository
from backend.driver_backend.repositories.tracking_repository import TrackingRepository
from backend.shared.utils import verify_password, create_access_token
from fastapi import HTTPException, status
from typing import Dict, Optional

class DriverService:
    """Business logic for driver operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.driver_repo = DriverRepository(db)
        self.shipment_repo = ShipmentRepository(db)
        self.tracking_repo = TrackingRepository(db)
    
    def register_driver(self, request):
        return self.driver_repo.create_driver(
        full_name=request.full_name,
        email=request.email,
        phone=request.phone,
        password=request.password
    )

    
    def authenticate_driver(self, email: str, password: str) -> Dict:
        """Authenticate driver and return token"""
        driver = self.driver_repo.get_driver_by_email(email)
        
        if not driver or not verify_password(password, driver.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        if not driver.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Driver account is inactive"
            )
        
        # Create JWT token
        token = create_access_token(
            data={"sub": driver.email, "role": driver.role.value, "id": driver.id}
        )
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "driver": {
                "id": driver.id,
                "email": driver.email,
                "full_name": driver.full_name,
                "phone": driver.phone
            }
        }
    
    def get_dashboard_data(self, driver_id: int) -> Dict:
        """Get driver dashboard statistics"""
        deliveries_today = self.shipment_repo.get_deliveries_today(driver_id)
        pending = self.shipment_repo.get_pending_count(driver_id)
        completed = self.shipment_repo.get_completed_count(driver_id)
        failed = self.shipment_repo.get_failed_count(driver_id)
        
        # Get last known location and current shipment
        last_location = None
        current_shipment = None
        assigned_shipments = self.shipment_repo.get_assigned_shipments(driver_id)
        
        if assigned_shipments:
            # Get first active shipment as current
            current = assigned_shipments[0]
            current_shipment = {
                "id": current.id,
                "shipment_number": current.shipment_number,
                "pickup_location": current.pickup_location,
                "delivery_location": current.delivery_location,
                "status": current.status.value if current.status else None
            }
            
            # Get last tracking location
            last_tracking = self.tracking_repo.get_last_location(current.id)
            if last_tracking:
                last_location = {
                    "latitude": last_tracking.latitude,
                    "longitude": last_tracking.longitude,
                    "location_name": last_tracking.location_name,
                    "timestamp": last_tracking.timestamp
                }
        
        return {
            "total_deliveries_today": deliveries_today,
            "pending_shipments": pending,
            "completed_shipments": completed,
            "failed_shipments": failed,
            "last_known_location": last_location,
            "current_shipment": current_shipment  # Added this field
        }   
    def update_location(
        self,
        latitude: float,
        longitude: float,
        shipment_id: Optional[int] = None,
        location_name: Optional[str] = None
    ) -> Dict:
        """Update driver location"""
        if shipment_id:
            self.tracking_repo.create_tracking_entry(
                shipment_id=shipment_id,
                latitude=latitude,
                longitude=longitude,
                location_name=location_name,
                status_update="Location updated by driver"
            )
        
        return {
            "message": "Location updated successfully",
            "latitude": latitude,
            "longitude": longitude
        }