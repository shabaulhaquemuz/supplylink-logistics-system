# ================================================================
# FILE: admin_backend/schemas/admin_shipment_schema.py
# ================================================================
"""
Admin Shipment Management Schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ShipmentListResponse(BaseModel):
    id: int
    shipment_number: str
    customer_id: int
    driver_id: Optional[int]
    pickup_location: str
    delivery_location: str
    cargo_type: Optional[str]
    weight: Optional[float]
    status: str
    estimated_delivery: Optional[datetime]
    actual_delivery: Optional[datetime]
    total_price: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True


class AssignDriverRequest(BaseModel):
    driver_id: int


class UpdateShipmentStatusRequest(BaseModel):
    status: str