"""This file contains all Pydantic schemas used by the Driver Backend for request and response validation.

It ensures that data coming from drivers — like login details or location updates — is always correctly formatted and safe.

DriverLoginRequest validates email/password when a driver tries to log in.

DriverLoginResponse defines the structured output returned after successful authentication.

LocationUpdate validates the driver’s live GPS coordinates and optional shipment/location info.

DriverDashboardResponse structures dashboard data such as deliveries, pending shipments, and last known location.

TrafficDelayRequest lets a driver report delays (traffic, weather, breakdown, etc.) with notes.

In simple words, this file defines all data shapes that the driver backend accepts and returns, keeping the API clean, predictable, and error-free.
"""
"""
Driver Request/Response Schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class DriverRegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str


class DriverRegisterResponse(BaseModel):
    id: int
    email: str
    full_name: str
    phone: str
    role: str = "driver"


class DriverLoginRequest(BaseModel):
    """Driver login request"""
    email: EmailStr
    password: str

class DriverLoginResponse(BaseModel):
    """Driver login response"""
    access_token: str
    token_type: str = "bearer"
    driver: dict

class LocationUpdate(BaseModel):
    """Driver location update"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    shipment_id: Optional[int] = None
    location_name: Optional[str] = None

class DriverDashboardResponse(BaseModel):
    """Driver dashboard data"""
    total_deliveries_today: int
    pending_shipments: int
    completed_shipments: int
    failed_shipments: int
    last_known_location: Optional[dict]
    current_shipment: Optional[dict]

class TrafficDelayRequest(BaseModel):
    """Report traffic delay"""
    shipment_id: int
    delay_reason: str
    notes: Optional[str] = None