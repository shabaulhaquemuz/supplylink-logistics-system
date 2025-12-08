"""
Pricing Controller - Handle price calculations
This file contains the API endpoint responsible for calculating shipment prices for the driver.

It receives inputs like distance, weight, shipment type, international mode, express delivery, and fuel price.

The controller ensures only authenticated drivers can calculate pricing using get_current_driver.

It forwards all pricing requests to the PricingService, which performs the actual cost calculations.

The endpoint returns a structured breakdown of base price, weight charge, fuel surcharge, mode surcharge, and final total.

It supports both domestic and international pricing logic.

The calculation is fully dynamic, based on real-world conditions like fuel price and express delivery.

In simple terms — this file exposes an API that gives the driver the exact shipping price estimate for any shipment.
"""
from fastapi import APIRouter, Depends
from backend.driver_backend.services.pricing_service import PricingService
from backend.driver_backend.schemas.pricing_schemas import (
    PriceCalculationRequest, PriceCalculationResponse
)
from backend.driver_backend.utils.dependencies import get_current_driver
from typing import Dict

router = APIRouter()

@router.post("/calculate-price", response_model=PriceCalculationResponse)
def calculate_shipment_price(
    request: PriceCalculationRequest,
    current_driver: Dict = Depends(get_current_driver)
):
    """
    Calculate shipment price based on:
    - Distance
    - Weight
    - Shipment type (domestic/international)
    - Mode (air/sea/truck)
    - Express delivery
    - Fuel price
    """
    service = PricingService()
    return service.calculate_price(
        distance_km=request.distance_km,
        weight_kg=request.weight_kg,
        shipment_type=request.shipment_type,
        international_mode=request.international_mode,
        is_express=request.is_express,
        fuel_price_per_liter=request.fuel_price_per_liter
    )