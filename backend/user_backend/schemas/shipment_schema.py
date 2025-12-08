# ================================================================
# FILE: user_backend/schemas/shipment_schema.py
# ================================================================
"""
Shipment-related Pydantic schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ShipmentCreate(BaseModel):
    pickup_location: str
    delivery_location: str
    cargo_type: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    is_home_pickup: bool = False
    is_home_delivery: bool = True
    is_cod: bool = False
    cod_amount: Optional[float] = None
    estimated_delivery: Optional[datetime] = None


class ShipmentResponse(BaseModel):
    id: int
    shipment_number: str
    customer_id: int
    pickup_location: str
    delivery_location: str
    cargo_type: Optional[str]
    weight: Optional[float]
    dimensions: Optional[str]
    status: str
    estimated_delivery: Optional[datetime]
    actual_delivery: Optional[datetime]
    is_cod: bool
    cod_amount: Optional[float]
    cod_status: Optional[str]
    base_price: Optional[float]
    fuel_surcharge: Optional[float]
    total_price: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TrackingResponse(BaseModel):
    id: int
    latitude: Optional[float]
    longitude: Optional[float]
    location_name: Optional[str]
    status_update: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True