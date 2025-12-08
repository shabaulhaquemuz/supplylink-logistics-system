"""
Pricing Service - Calculate shipment prices
This file contains the pricing engine for calculating shipment costs based on distance, weight, delivery mode, and fuel rates.

It defines base rates for domestic and international shipments (air, sea, truck), following real logistics pricing patterns.

The service applies a weight multiplier, making heavier parcels cost more as distance increases.

International air shipments automatically get an additional mode surcharge because they are premium and faster.

A fuel surcharge is added based on real fuel consumption (distance divided by average km/liter).

Optional express delivery applies a percentage-based surcharge for fast delivery.

The method returns a full price breakdown, including all components and factors used.

In simple words — this file is the smart calculator that computes final delivery costs with transparent, itemized logic.

"""
from typing import Dict

class PricingService:
    """Business logic for price calculation"""
    
    # Base rates (INR per km)
    BASE_RATE_DOMESTIC = 15.0
    BASE_RATE_INTERNATIONAL_AIR = 50.0
    BASE_RATE_INTERNATIONAL_SEA = 30.0
    BASE_RATE_INTERNATIONAL_TRUCK = 20.0
    
    # Weight multiplier (INR per kg per km)
    WEIGHT_MULTIPLIER = 2.0
    
    # Express delivery surcharge (%)
    EXPRESS_SURCHARGE_PERCENT = 30.0
    
    def __init__(self):
        pass
    
    def calculate_price(
        self,
        distance_km: float,
        weight_kg: float,
        shipment_type: str,
        international_mode: str = None,
        is_express: bool = False,
        fuel_price_per_liter: float = 100.0
    ) -> Dict:
        """
        Calculate shipment price based on multiple factors
        
        Args:
            distance_km: Distance in kilometers
            weight_kg: Weight in kilograms
            shipment_type: 'domestic' or 'international'
            international_mode: 'air', 'sea', or 'truck' (for international)
            is_express: Whether express delivery
            fuel_price_per_liter: Current fuel price
        
        Returns:
            Dictionary with price breakdown
        """
        
        # Determine base rate
        if shipment_type == "domestic":
            base_rate = self.BASE_RATE_DOMESTIC
        else:
            if international_mode == "air":
                base_rate = self.BASE_RATE_INTERNATIONAL_AIR
            elif international_mode == "sea":
                base_rate = self.BASE_RATE_INTERNATIONAL_SEA
            elif international_mode == "truck":
                base_rate = self.BASE_RATE_INTERNATIONAL_TRUCK
            else:
                base_rate = self.BASE_RATE_DOMESTIC
        
        # Calculate base price
        base_price = base_rate * distance_km
        
        # Weight charge
        weight_charge = weight_kg * self.WEIGHT_MULTIPLIER * distance_km
        
        # Mode surcharge (for international air)
        mode_surcharge = 0.0
        if shipment_type == "international" and international_mode == "air":
            mode_surcharge = base_price * 0.25  # 25% surcharge for air
        
        # Fuel surcharge (based on fuel price and distance)
        # Assuming average of 8 km per liter
        fuel_consumption = distance_km / 8.0
        fuel_surcharge = fuel_consumption * fuel_price_per_liter
        
        # Express charge
        express_charge = 0.0
        if is_express:
            express_charge = (base_price + weight_charge) * (self.EXPRESS_SURCHARGE_PERCENT / 100)
        
        # Total price
        total_price = base_price + weight_charge + mode_surcharge + fuel_surcharge + express_charge
        
        return {
            "base_price": round(base_price, 2),
            "weight_charge": round(weight_charge, 2),
            "mode_surcharge": round(mode_surcharge, 2),
            "fuel_surcharge": round(fuel_surcharge, 2),
            "express_charge": round(express_charge, 2),
            "total_price": round(total_price, 2),
            "breakdown": {
                "distance_km": distance_km,
                "weight_kg": weight_kg,
                "base_rate_per_km": base_rate,
                "shipment_type": shipment_type,
                "international_mode": international_mode,
                "is_express": is_express,
                "fuel_price_per_liter": fuel_price_per_liter
            }
        }


