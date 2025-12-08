"""
Shipment Repository - All shipment DB operations
This file contains the repository layer that handles all shipment-related database operations for drivers.

It provides reusable, clean functions so services don’t need to write SQL queries directly.

get_assigned_shipments() returns all active shipments assigned to a driver (assigned → out for delivery).

Other methods update shipment status, such as picked up, delivered, or failed deliveries.

It also includes functions for COD collection, customs clearance updates, and reporting delays.

Every update sets timestamps automatically to maintain delivery history accurately.

It provides dashboard metrics like today's deliveries, pending count, completed and failed counts.

In simple words — this file is the shipment database helper, enabling the driver backend to read/update shipment information efficiently.
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from backend.shared.models import Shipment, User
from backend.driver_backend.utils.enums import ShipmentStatus, CustomsStatus, CODStatus
from typing import List, Optional
from datetime import datetime, date

class ShipmentRepository:
    """Handle all shipment database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_assigned_shipments(self, driver_id: int) -> List[Shipment]:
        """Get all shipments assigned to driver"""
        return self.db.query(Shipment).filter(
            Shipment.driver_id == driver_id,
            Shipment.status.in_([
                ShipmentStatus.ASSIGNED,
                ShipmentStatus.PICKED_UP,
                ShipmentStatus.IN_TRANSIT,
                ShipmentStatus.OUT_FOR_DELIVERY
            ])
        ).all()
    
    def get_shipment_by_id(self, shipment_id: int) -> Optional[Shipment]:
        """Get shipment by ID"""
        return self.db.query(Shipment).filter(Shipment.id == shipment_id).first()
    
    def update_shipment_status(self, shipment_id: int, status: ShipmentStatus) -> bool:
        """Update shipment status"""
        shipment = self.get_shipment_by_id(shipment_id)
        if shipment:
            shipment.status = status
            shipment.updated_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    def mark_picked_up(self, shipment_id: int) -> bool:
        """Mark shipment as picked up"""
        shipment = self.get_shipment_by_id(shipment_id)
        if shipment:
            shipment.status = ShipmentStatus.PICKED_UP
            shipment.pickup_completed_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    def mark_delivered(self, shipment_id: int) -> bool:
        """Mark shipment as delivered"""
        shipment = self.get_shipment_by_id(shipment_id)
        if shipment:
            shipment.status = ShipmentStatus.DELIVERED
            shipment.actual_delivery = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    def mark_failed(self, shipment_id: int, reason: str, notes: Optional[str]) -> bool:
        """Mark delivery as failed"""
        shipment = self.get_shipment_by_id(shipment_id)
        if shipment:
            shipment.status = ShipmentStatus.FAILED
            shipment.failure_reason = reason
            shipment.failure_notes = notes
            shipment.delivery_attempted_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    def mark_cod_collected(self, shipment_id: int, amount: float) -> bool:
        """Mark COD collected"""
        shipment = self.get_shipment_by_id(shipment_id)
        if shipment:
            shipment.cod_status = CODStatus.COLLECTED
            shipment.cod_collected_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    def update_customs_status(self, shipment_id: int, status: CustomsStatus) -> bool:
        """Update customs clearance status"""
        shipment = self.get_shipment_by_id(shipment_id)
        if shipment:
            shipment.customs_clearance_status = status
            if status == CustomsStatus.CLEARED:
                shipment.customs_cleared_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    def report_delay(self, shipment_id: int, reason: str, notes: Optional[str]) -> bool:
        """Report traffic/delay"""
        shipment = self.get_shipment_by_id(shipment_id)
        if shipment:
            shipment.delay_reason = reason
            shipment.delay_notes = notes
            shipment.delay_reported_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    def get_deliveries_today(self, driver_id: int) -> int:
        """Get total deliveries today"""
        today = date.today()
        return self.db.query(Shipment).filter(
            Shipment.driver_id == driver_id,
            Shipment.status == ShipmentStatus.DELIVERED,
            func.date(Shipment.actual_delivery) == today
        ).count()
    
    def get_pending_count(self, driver_id: int) -> int:
        """Get pending shipments count"""
        return self.db.query(Shipment).filter(
            Shipment.driver_id == driver_id,
            Shipment.status.in_([ShipmentStatus.ASSIGNED, ShipmentStatus.IN_TRANSIT])
        ).count()
    
    def get_completed_count(self, driver_id: int) -> int:
        """Get completed shipments count"""
        return self.db.query(Shipment).filter(
            Shipment.driver_id == driver_id,
            Shipment.status == ShipmentStatus.DELIVERED
        ).count()
    
    def get_failed_count(self, driver_id: int) -> int:
        """Get failed deliveries count"""
        return self.db.query(Shipment).filter(
            Shipment.driver_id == driver_id,
            Shipment.status == ShipmentStatus.FAILED
        ).count()
    def update_status(self, shipment_id: int, new_status: ShipmentStatus) -> bool:
        """Update shipment status"""
        shipment = self.get_shipment_by_id(shipment_id)
        if shipment:
            shipment.status = new_status
            shipment.updated_at = datetime.utcnow()
            self.db.commit()
            return True
        return False