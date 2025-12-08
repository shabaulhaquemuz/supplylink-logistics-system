"""
Pricing Request/Response Schemas
This file defines all Pydantic schemas used for shipment price calculation in the driver backend.

PriceCalculationRequest ensures all inputs needed for price computation—distance, weight, mode, and fuel price—are valid and correctly formatted.

It supports both domestic and international shipments and includes optional express delivery and transport mode fields.

Validation rules like gt=0 ensure no invalid or negative values are passed into the pricing engine.

PriceCalculationResponse structures the complete price breakdown returned by the system.

It includes separate fields for base cost, weight charge, express fee, fuel surcharge, and international mode surcharge.

The breakdown dictionary allows flexible expansion of pricing logic in the future without changing API structure.

In simple words — this file defines how pricing inputs are sent and how detailed pricing results are returned, keeping pricing logic clean and organized.
"""
from pydantic import BaseModel, Field
from typing import Optional

class PriceCalculationRequest(BaseModel):
    """Calculate shipment price"""
    distance_km: float = Field(..., gt=0)
    weight_kg: float = Field(..., gt=0)
    shipment_type: str  # domestic/international
    international_mode: Optional[str] = None  # air/sea/truck
    is_express: bool = False
    fuel_price_per_liter: float = Field(default=100.0, gt=0)

class PriceCalculationResponse(BaseModel):
    """Price breakdown"""
    base_price: float
    weight_charge: float
    mode_surcharge: float
    fuel_surcharge: float
    express_charge: float
    total_price: float
    breakdown: dict