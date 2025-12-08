# ================================================================
# FILE: admin_backend/services/admin_shipment_service.py
# ================================================================
"""
Admin Shipment Management Service
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from backend.shared.models import Shipment, User, UserRole
from backend.driver_backend.utils.enums import ShipmentStatus


class AdminShipmentService:
    def __init__(self):
        pass

    def get_all_shipments(self, db: Session) -> List[Shipment]:
        """Get all shipments in the system"""
        shipments = db.query(Shipment).order_by(Shipment.created_at.desc()).all()
        return shipments

    def get_shipment_by_id(self, shipment_id: int, db: Session) -> Shipment:
        """Get specific shipment by ID"""
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        
        if not shipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipment not found"
            )
        
        return shipment

    def assign_driver_to_shipment(self, shipment_id: int, driver_id: int, db: Session) -> Shipment:
        """Assign a driver to a shipment"""
        # Verify shipment exists
        shipment = self.get_shipment_by_id(shipment_id, db)

        # Verify driver exists and has DRIVER role
        driver = db.query(User).filter(
            User.id == driver_id,
            User.role == UserRole.DRIVER
        ).first()

        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )

        if not driver.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot assign inactive driver"
            )

        # Assign driver
        shipment.driver_id = driver_id
        
        # Update status if still pending
        if shipment.status == ShipmentStatus.PENDING:
            shipment.status = ShipmentStatus.PICKED_UP

        db.commit()
        db.refresh(shipment)

        return shipment

    def update_shipment_status(self, shipment_id: int, new_status: str, db: Session) -> Shipment:
        """Update shipment status"""
        shipment = self.get_shipment_by_id(shipment_id, db)

        # Validate status
        try:
            status_enum = ShipmentStatus(new_status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Valid options: {[s.value for s in ShipmentStatus]}"
            )

        shipment.status = status_enum

        # If marked as delivered, set actual delivery time
        if status_enum == ShipmentStatus.DELIVERED:
            from datetime import datetime
            shipment.actual_delivery = datetime.utcnow()

        db.commit()
        db.refresh(shipment)

        return shipment