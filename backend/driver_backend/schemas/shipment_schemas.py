"""
Shipment Request/Response Schemas
This file defines all Pydantic schemas related to shipment operations for the driver backend.

ShipmentListResponse structures the summary view of shipments shown in the driver’s list page.

ShipmentDetailResponse provides the full detailed information of a single shipment, including COD, international mode, and customer details.

Pickup/delivery workflows are handled through schemas like MarkPickedUpRequest and MarkDeliveredRequest, which cleanly validate driver input.

Failed delivery reasons are managed using MarkFailedRequest, ensuring reason + notes are always provided in a structured format.

COD handling is supported through CODCollectionRequest which validates collected amount for cash-on-delivery shipments.

International logistics is supported through CustomsClearanceRequest and PortPickupRequest, making the system ready for air/sea/truck imports.

In simple words — this file defines ALL request and response shapes for shipment operations, ensuring safe, consistent data flow between app and server.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from backend.driver_backend.utils.enums import (
    ShipmentStatus, FailureReason, CustomsStatus, CODStatus
)

class ShipmentListResponse(BaseModel):
    """List of shipments for driver"""
    id: int
    shipment_number: str
    pickup_location: str
    delivery_location: str
    status: str
    estimated_delivery: Optional[datetime]
    is_cod: bool
    cod_amount: Optional[float]
    shipment_type: str
    
    class Config:
        from_attributes = True

class ShipmentDetailResponse(BaseModel):
    """Detailed shipment info"""
    id: int
    shipment_number: str
    pickup_location: str
    delivery_location: str
    cargo_type: str
    weight: float
    status: str
    customer_name: str
    customer_phone: str
    is_cod: bool
    cod_amount: Optional[float]
    is_home_pickup: Optional[bool] = False  # ADD Optional + default
    is_home_delivery: Optional[bool] = True  # ADD Optional + default
    shipment_type: str
    international_mode: Optional[str]
    port_of_entry: Optional[str]
    customs_clearance_status: Optional[str]
    
    class Config:
        from_attributes = True

class MarkPickedUpRequest(BaseModel):
    """Mark shipment as picked up"""
    shipment_id: int
    notes: Optional[str] = None

class MarkDeliveredRequest(BaseModel):
    """Mark shipment as delivered"""
    shipment_id: int
    signature: Optional[str] = None  # Base64 signature image
    photo_proof: Optional[str] = None  # Base64 image
    notes: Optional[str] = None

class MarkFailedRequest(BaseModel):
    """Mark delivery as failed"""
    shipment_id: int
    failure_reason: FailureReason
    notes: Optional[str] = None

class CODCollectionRequest(BaseModel):
    """Mark COD collected"""
    shipment_id: int
    amount_collected: float

class CustomsClearanceRequest(BaseModel):
    """Confirm customs clearance"""
    shipment_id: int
    clearance_notes: Optional[str] = None

class PortPickupRequest(BaseModel):
    """Confirm pickup from port/airport"""
    shipment_id: int
    port_location: str
    notes: Optional[str] = None