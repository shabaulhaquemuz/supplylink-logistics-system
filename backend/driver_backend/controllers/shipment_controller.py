"""
Shipment Controller - Handle shipment operations
This file contains all API endpoints that deal with driver shipment operations.

It allows drivers to view assigned shipments, see shipment details, and perform required actions.

The controller uses JWT authentication via get_current_driver to ensure only assigned drivers can access shipments.

Endpoints allow marking shipments as picked up, delivered, or failed, depending on real delivery events.

It also provides APIs for COD collection, customs clearance, and port/airport pickups for international shipments.

Tracking updates like failure notes, delivery proof, and status changes are handled through the service layer.

There is a dedicated endpoint for reporting traffic delays or issues during transit.

In simple words — this file exposes all shipment-related actions a driver can perform while delivering packages.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.shared.database import get_db
from backend.driver_backend.services.shipment_service import ShipmentService
from backend.driver_backend.schemas.shipment_schemas import (
    ShipmentListResponse, ShipmentDetailResponse,
    MarkPickedUpRequest, MarkDeliveredRequest, MarkFailedRequest,
    CODCollectionRequest, CustomsClearanceRequest, PortPickupRequest
)
from backend.driver_backend.schemas.driver_schemas import TrafficDelayRequest
from backend.driver_backend.utils.dependencies import get_current_driver
from typing import List, Dict

router = APIRouter()

@router.get("/shipments", response_model=List[ShipmentListResponse])
def get_assigned_shipments(
    current_driver: Dict = Depends(get_current_driver),
    db: Session = Depends(get_db)
):
    """
    Get all shipments assigned to the driver
    """
    service = ShipmentService(db)
    return service.get_assigned_shipments(current_driver["id"])

@router.get("/shipments/{shipment_id}", response_model=ShipmentDetailResponse)
def get_shipment_details(
    shipment_id: int,
    current_driver: Dict = Depends(get_current_driver),
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific shipment
    """
    service = ShipmentService(db)
    return service.get_shipment_details(shipment_id, current_driver["id"])

@router.post("/shipments/pickup")
def mark_shipment_picked_up(
    request: MarkPickedUpRequest,
    current_driver: Dict = Depends(get_current_driver),
    db: Session = Depends(get_db)
):
    """
    Mark shipment as picked up
    Used when driver picks up the shipment from sender
    """
    service = ShipmentService(db)
    return service.mark_picked_up(
        request.shipment_id,
        current_driver["id"],
        request.notes
    )

@router.post("/shipments/in-transit")
def mark_shipment_in_transit(
    request: MarkPickedUpRequest,  # Can reuse this schema (shipment_id + notes)
    current_driver: Dict = Depends(get_current_driver),
    db: Session = Depends(get_db)
):
    """
    Mark shipment as in transit
    Used when driver starts moving with the shipment
    """
    service = ShipmentService(db)
    return service.mark_in_transit(
        request.shipment_id,
        current_driver["id"],
        request.notes
    )

@router.post("/shipments/out-for-delivery")
def mark_shipment_out_for_delivery(
    request: MarkPickedUpRequest,  # Can reuse this schema
    current_driver: Dict = Depends(get_current_driver),
    db: Session = Depends(get_db)
):
    """
    Mark shipment as out for delivery
    Used when driver is near delivery location
    """
    service = ShipmentService(db)
    return service.mark_out_for_delivery(
        request.shipment_id,
        current_driver["id"],
        request.notes
    )
@router.post("/shipments/deliver")
def mark_shipment_delivered(
    request: MarkDeliveredRequest,
    current_driver: Dict = Depends(get_current_driver),
    db: Session = Depends(get_db)
):
    """
    Mark shipment as delivered
    Requires signature and/or photo proof
    """
    service = ShipmentService(db)
    return service.mark_delivered(
        request.shipment_id,
        current_driver["id"],
        request.signature,
        request.photo_proof,
        request.notes
    )

@router.post("/shipments/fail")
def mark_delivery_failed(
    request: MarkFailedRequest,
    current_driver: Dict = Depends(get_current_driver),
    db: Session = Depends(get_db)
):
    """
    Mark delivery as failed
    Required when delivery cannot be completed
    """
    service = ShipmentService(db)
    return service.mark_failed(
        request.shipment_id,
        current_driver["id"],
        request.failure_reason.value,
        request.notes
    )

@router.post("/shipments/cod-collect")
def collect_cod_payment(
    request: CODCollectionRequest,
    current_driver: Dict = Depends(get_current_driver),
    db: Session = Depends(get_db)
):
    """
    Mark Cash-on-Delivery payment collected
    """
    service = ShipmentService(db)
    return service.collect_cod(
        request.shipment_id,
        current_driver["id"],
        request.amount_collected
    )

@router.post("/shipments/customs-clearance")
def confirm_customs_clearance(
    request: CustomsClearanceRequest,
    current_driver: Dict = Depends(get_current_driver),
    db: Session = Depends(get_db)
):
    """
    Confirm customs clearance completed
    For international shipments
    """
    service = ShipmentService(db)
    return service.confirm_customs_clearance(
        request.shipment_id,
        current_driver["id"],
        request.clearance_notes
    )

@router.post("/shipments/port-pickup")
def confirm_port_pickup(
    request: PortPickupRequest,
    current_driver: Dict = Depends(get_current_driver),
    db: Session = Depends(get_db)
):
    """
    Confirm pickup from port/airport/warehouse
    For international shipments
    """
    service = ShipmentService(db)
    return service.confirm_port_pickup(
        request.shipment_id,
        current_driver["id"],
        request.port_location,
        request.notes
    )

@router.post("/shipments/report-delay")
def report_traffic_delay(
    request: TrafficDelayRequest,
    current_driver: Dict = Depends(get_current_driver),
    db: Session = Depends(get_db)
):
    """
    Report traffic delay or other issues
    """
    service = ShipmentService(db)
    return service.report_delay(
        request.shipment_id,
        current_driver["id"],
        request.delay_reason,
        request.notes
    )