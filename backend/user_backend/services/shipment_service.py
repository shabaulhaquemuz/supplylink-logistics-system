# ================================================================
# FILE: user_backend/services/shipment_service.py
# ================================================================
"""
Shipment Service - Handles all shipment-related business logic
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
import secrets

from backend.shared.models import Shipment, TrackingData, User
from backend.driver_backend.utils.enums import ShipmentStatus
from backend.user_backend.schemas.shipment_schema import ShipmentCreate


class ShipmentService:
    def __init__(self):
        pass

    def generate_shipment_number(self) -> str:
        """Generate unique shipment number"""
        return f"SHP{secrets.token_hex(4).upper()}"

    def calculate_shipment_price(self, weight: Optional[float], distance: float = 100.0) -> dict:
        """Calculate shipment pricing"""
        base_price = 50.0
        if weight:
            base_price += weight * 2.0
        fuel_surcharge = base_price * 0.15
        total_price = base_price + fuel_surcharge

        return {
            "base_price": round(base_price, 2),
            "fuel_surcharge": round(fuel_surcharge, 2),
            "total_price": round(total_price, 2)
        }

    def create_shipment(self, shipment_data: ShipmentCreate, current_user: User, db: Session) -> Shipment:
        """Create a new shipment"""
        # Calculate pricing
        pricing = self.calculate_shipment_price(shipment_data.weight)
    
        # Calculate estimated delivery (e.g., 5 days from now)
        from datetime import datetime, timedelta
        estimated_delivery = datetime.utcnow() + timedelta(days=5)
    
        # If heavy cargo, add more days
        if shipment_data.weight and shipment_data.weight > 50:
         estimated_delivery += timedelta(days=2)
    
        # Create shipment
        new_shipment = Shipment(
            shipment_number=self.generate_shipment_number(),
            customer_id=current_user.id,
            pickup_location=shipment_data.pickup_location,
            delivery_location=shipment_data.delivery_location,
            cargo_type=shipment_data.cargo_type,
            weight=shipment_data.weight,
            dimensions=shipment_data.dimensions,
            status=ShipmentStatus.PENDING,
            estimated_delivery=estimated_delivery,  # System-calculated
            is_home_pickup=shipment_data.is_home_pickup,
            is_home_delivery=shipment_data.is_home_delivery,
            is_cod=shipment_data.is_cod,
            cod_amount=shipment_data.cod_amount,
            base_price=pricing["base_price"],
            fuel_surcharge=pricing["fuel_surcharge"],
            total_price=pricing["total_price"]
        )
    
        db.add(new_shipment)
        db.commit()
        db.refresh(new_shipment)
    
        return new_shipment

    def get_user_shipments(self, user_id: int, db: Session) -> List[Shipment]:
        """Get all shipments for a user"""
        shipments = db.query(Shipment).filter(
            Shipment.customer_id == user_id
        ).order_by(Shipment.created_at.desc()).all()

        return shipments

    def get_shipment_by_id(self, shipment_id: int, user_id: int, db: Session) -> Shipment:
        """Get specific shipment by ID"""
        shipment = db.query(Shipment).filter(
            Shipment.id == shipment_id,
            Shipment.customer_id == user_id
        ).first()

        if not shipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipment not found"
            )

        return shipment

    def get_shipment_tracking(self, shipment_id: int, user_id: int, db: Session) -> List[TrackingData]:
        """Get tracking data for a shipment"""
        # Verify shipment belongs to user
        shipment = self.get_shipment_by_id(shipment_id, user_id, db)

        # Get tracking data
        tracking_data = db.query(TrackingData).filter(
            TrackingData.shipment_id == shipment_id
        ).order_by(TrackingData.timestamp.desc()).all()

        return tracking_data

    def cancel_shipment(self, shipment_id: int, user_id: int, db: Session) -> None:
        """Cancel a pending shipment"""
        shipment = self.get_shipment_by_id(shipment_id, user_id, db)

        if shipment.status != ShipmentStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only cancel pending shipments"
            )

        db.delete(shipment)
        db.commit()