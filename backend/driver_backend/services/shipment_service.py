"""
Shipment Service - Business logic for shipment operations
This file contains the business logic for all shipment-related actions a driver can perform.

It sits between the controllers and repositories, so it applies rules before updating the database.

get_assigned_shipments() and get_shipment_details() return shipment information after verifying driver access.

mark_picked_up(), mark_delivered(), and mark_failed() update shipment status and automatically create tracking logs.

It validates whether the driver is allowed to perform each action (status check + assigned driver check).

collect_cod() ensures COD shipments have correct amount before marking them collected.

confirm_customs_clearance() and confirm_port_pickup() handle international shipment workflows like customs and port handling.

In simple words – this service contains all rules for shipment lifecycle, protecting data integrity and ensuring only correct status transitions happen.
"""
from sqlalchemy.orm import Session
from backend.driver_backend.repositories.shipment_repository import ShipmentRepository
from backend.driver_backend.repositories.tracking_repository import TrackingRepository
from backend.driver_backend.utils.enums import ShipmentStatus, CustomsStatus
from fastapi import HTTPException, status
from typing import List, Dict, Optional

class ShipmentService:
    """Business logic for shipment operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.shipment_repo = ShipmentRepository(db)
        self.tracking_repo = TrackingRepository(db)
    
    def get_assigned_shipments(self, driver_id: int) -> List[Dict]:
        """Get all assigned shipments for driver"""
        shipments = self.shipment_repo.get_assigned_shipments(driver_id)
        return [self._format_shipment(s) for s in shipments]
    
    def get_shipment_details(self, shipment_id: int, driver_id: int) -> Dict:
        """Get detailed shipment information"""
        shipment = self.shipment_repo.get_shipment_by_id(shipment_id)
        
        if not shipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipment not found"
            )
        
        if shipment.driver_id != driver_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not assigned to this shipment"
            )
        
        return self._format_shipment_detail(shipment)
    
    def mark_picked_up(self, shipment_id: int, driver_id: int, notes: Optional[str]) -> Dict:
        """Mark shipment as picked up"""
        shipment = self._validate_shipment_access(shipment_id, driver_id)
        
        if shipment.status != ShipmentStatus.ASSIGNED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot mark as picked up. Current status: {shipment.status}"
            )
        
        success = self.shipment_repo.mark_picked_up(shipment_id)
        
        if success:
            # Create tracking entry
            self.tracking_repo.create_tracking_entry(
                shipment_id=shipment_id,
                latitude=0.0,  # Driver should send location separately
                longitude=0.0,
                status_update=f"Shipment picked up. Notes: {notes or 'None'}"
            )
        
        return {"message": "Shipment marked as picked up", "shipment_id": shipment_id}
    
    def mark_in_transit(self, shipment_id: int, driver_id: int, notes: Optional[str]) -> Dict:
        """Mark shipment as in transit"""
        shipment = self._validate_shipment_access(shipment_id, driver_id)
        
        if shipment.status != ShipmentStatus.PICKED_UP:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot mark as in transit. Current status: {shipment.status}"
            )
        
        success = self.shipment_repo.update_status(shipment_id, ShipmentStatus.IN_TRANSIT)
        
        if success:
            self.tracking_repo.create_tracking_entry(
                shipment_id=shipment_id,
                latitude=0.0,
                longitude=0.0,
                status_update=f"Shipment in transit. Notes: {notes or 'None'}"
            )
        
        return {"message": "Shipment marked as in transit", "shipment_id": shipment_id}

    def mark_out_for_delivery(self, shipment_id: int, driver_id: int, notes: Optional[str]) -> Dict:
        """Mark shipment as out for delivery"""
        shipment = self._validate_shipment_access(shipment_id, driver_id)
        
        if shipment.status != ShipmentStatus.IN_TRANSIT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot mark as out for delivery. Current status: {shipment.status}"
            )
        
        success = self.shipment_repo.update_status(shipment_id, ShipmentStatus.OUT_FOR_DELIVERY)
        
        if success:
            self.tracking_repo.create_tracking_entry(
                shipment_id=shipment_id,
                latitude=0.0,
                longitude=0.0,
                status_update=f"Out for delivery. Notes: {notes or 'None'}"
            )
        
        return {"message": "Shipment marked as out for delivery", "shipment_id": shipment_id}
    def mark_delivered(
        self,
        shipment_id: int,
        driver_id: int,
        signature: Optional[str],
        photo_proof: Optional[str],
        notes: Optional[str]
    ) -> Dict:
        """Mark shipment as delivered"""
        shipment = self._validate_shipment_access(shipment_id, driver_id)
        
        if shipment.status not in [ShipmentStatus.IN_TRANSIT, ShipmentStatus.OUT_FOR_DELIVERY]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot mark as delivered. Current status: {shipment.status}"
            )
        
        success = self.shipment_repo.mark_delivered(shipment_id)
        
        if success:
            self.tracking_repo.create_tracking_entry(
                shipment_id=shipment_id,
                latitude=0.0,
                longitude=0.0,
                status_update=f"Delivered successfully. Notes: {notes or 'None'}"
            )
        
        return {"message": "Shipment delivered successfully", "shipment_id": shipment_id}
    
    def mark_failed(
        self,
        shipment_id: int,
        driver_id: int,
        failure_reason: str,
        notes: Optional[str]
    ) -> Dict:
        """Mark delivery as failed"""
        shipment = self._validate_shipment_access(shipment_id, driver_id)
        
        success = self.shipment_repo.mark_failed(shipment_id, failure_reason, notes)
        
        if success:
            self.tracking_repo.create_tracking_entry(
                shipment_id=shipment_id,
                latitude=0.0,
                longitude=0.0,
                status_update=f"Delivery failed: {failure_reason}. Notes: {notes or 'None'}"
            )
        
        return {"message": "Delivery marked as failed", "shipment_id": shipment_id}
    
    def collect_cod(self, shipment_id: int, driver_id: int, amount: float) -> Dict:
        """Mark COD collected"""
        shipment = self._validate_shipment_access(shipment_id, driver_id)
        
        if not shipment.is_cod:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This shipment is not COD"
            )
        
        if amount != shipment.cod_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Amount mismatch. Expected: {shipment.cod_amount}, Got: {amount}"
            )
        
        success = self.shipment_repo.mark_cod_collected(shipment_id, amount)
        
        return {"message": "COD collected successfully", "amount": amount}
    
    def confirm_customs_clearance(self, shipment_id: int, driver_id: int, notes: Optional[str]) -> Dict:
        """Confirm customs clearance completed"""
        shipment = self._validate_shipment_access(shipment_id, driver_id)
        
        if shipment.shipment_type != "international":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This is not an international shipment"
            )
        
        success = self.shipment_repo.update_customs_status(shipment_id, CustomsStatus.CLEARED)
        
        if success:
            self.tracking_repo.create_tracking_entry(
                shipment_id=shipment_id,
                latitude=0.0,
                longitude=0.0,
                status_update=f"Customs cleared. Notes: {notes or 'None'}"
            )
        
        return {"message": "Customs clearance confirmed"}
    
    def confirm_port_pickup(
        self,
        shipment_id: int,
        driver_id: int,
        port_location: str,
        notes: Optional[str]
    ) -> Dict:
        """Confirm pickup from port/airport"""
        shipment = self._validate_shipment_access(shipment_id, driver_id)
        
        success = self.shipment_repo.mark_picked_up(shipment_id)
        
        if success:
            self.tracking_repo.create_tracking_entry(
                shipment_id=shipment_id,
                latitude=0.0,
                longitude=0.0,
                location_name=port_location,
                status_update=f"Picked up from {port_location}. Notes: {notes or 'None'}"
            )
        
        return {"message": f"Pickup from {port_location} confirmed"}
    
    def report_delay(
        self,
        shipment_id: int,
        driver_id: int,
        delay_reason: str,
        notes: Optional[str]
    ) -> Dict:
        """Report traffic/delay"""
        shipment = self._validate_shipment_access(shipment_id, driver_id)
        
        success = self.shipment_repo.report_delay(shipment_id, delay_reason, notes)
        
        if success:
            self.tracking_repo.create_tracking_entry(
                shipment_id=shipment_id,
                latitude=0.0,
                longitude=0.0,
                status_update=f"Delay reported: {delay_reason}. Notes: {notes or 'None'}"
            )
        
        return {"message": "Delay reported successfully"}

    def _validate_shipment_access(self, shipment_id: int, driver_id: int):
        """Validate driver has access to shipment"""
        shipment = self.shipment_repo.get_shipment_by_id(shipment_id)
        
        if not shipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipment not found"
            )
        
        if shipment.driver_id != driver_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not assigned to this shipment"
            )
        
        return shipment

    def _format_shipment(self, shipment) -> Dict:
        """Format shipment for list view"""
        return {
            "id": shipment.id,
            "shipment_number": shipment.shipment_number,
            "pickup_location": shipment.pickup_location,
            "delivery_location": shipment.delivery_location,
            "status": shipment.status.value if shipment.status else None,
            "estimated_delivery": shipment.estimated_delivery,
            "is_cod": shipment.is_cod,
            "cod_amount": shipment.cod_amount,
            "shipment_type": shipment.shipment_type.value if shipment.shipment_type else None
        }

    def _format_shipment_detail(self, shipment) -> Dict:
        """Format shipment for detail view"""
        return {
            "id": shipment.id,
            "shipment_number": shipment.shipment_number,
            "pickup_location": shipment.pickup_location,
            "delivery_location": shipment.delivery_location,
            "cargo_type": shipment.cargo_type,
            "weight": shipment.weight,
            "status": shipment.status.value if shipment.status else None,
            "customer_name": shipment.customer.full_name if shipment.customer else "N/A",
            "customer_phone": shipment.customer.phone if shipment.customer else "N/A",
            "is_cod": shipment.is_cod,
            "cod_amount": shipment.cod_amount,
            "is_home_pickup": shipment.is_home_pickup,
            "is_home_delivery": shipment.is_home_delivery,
            "shipment_type": shipment.shipment_type.value if shipment.shipment_type else None,
            "international_mode": shipment.international_mode.value if shipment.international_mode else None,
            "port_of_entry": shipment.port_of_entry.value if shipment.port_of_entry else None,
            "customs_clearance_status": shipment.customs_clearance_status.value if shipment.customs_clearance_status else None
        }