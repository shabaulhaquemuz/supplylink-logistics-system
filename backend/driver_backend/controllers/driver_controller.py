"""
Driver Controller - Handle driver-related routes
This file defines all HTTP API endpoints related to drivers, such as login, dashboard, and location updates.

It uses FastAPI’s APIRouter to keep driver routes separate and organized.

driver_login() authenticates a driver and returns a JWT token using the DriverService.

get_dashboard() retrieves driver analytics like deliveries, pending shipments, and last location.

It uses get_current_driver to ensure the driver is authenticated before accessing protected endpoints.

update_location() saves the driver’s real-time GPS location for live tracking.

Each endpoint delegates logic to the service layer, making the controller clean and thin.

In simple words — this file is the API layer that exposes driver operations to the frontend or mobile app.
"""
"""
Driver Controller - Handle driver-related routes
"""

"""
Driver Controller - Handle driver-related routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict

# Database + Service
from backend.shared.database import get_db
from backend.driver_backend.services.driver_service import DriverService

# Driver Schemas
from backend.driver_backend.schemas.driver_schemas import (
    DriverLoginRequest, DriverLoginResponse, LocationUpdate,
    DriverDashboardResponse, TrafficDelayRequest,
    DriverRegisterRequest, DriverRegisterResponse
)

# Auth Dependency
from backend.driver_backend.utils.dependencies import get_current_driver

# ==================== CREATE ROUTER ====================
router = APIRouter(tags=["Driver Operations"])


# ==================== DRIVER REGISTRATION ====================
@router.post("/register", response_model=DriverRegisterResponse)
def register_driver(
    request: DriverRegisterRequest,
    db: Session = Depends(get_db)
):
    service = DriverService(db)
    driver = service.register_driver(request)

    if not driver:
        raise HTTPException(status_code=400, detail="Email already exists")

    return driver


# ==================== DRIVER LOGIN ====================
@router.post("/login", response_model=DriverLoginResponse)
def driver_login(
    request: DriverLoginRequest,
    db: Session = Depends(get_db)
):
    service = DriverService(db)
    return service.authenticate_driver(request.email, request.password)


# ==================== DASHBOARD ====================
@router.get("/dashboard", response_model=DriverDashboardResponse)
def get_dashboard(
    current_driver: Dict = Depends(get_current_driver),
    db: Session = Depends(get_db)
):
    service = DriverService(db)
    return service.get_dashboard_data(current_driver["id"])


# ==================== UPDATE LOCATION ====================
@router.post("/location")
def update_location(
    location: LocationUpdate,
    current_driver: Dict = Depends(get_current_driver),
    db: Session = Depends(get_db)
):
    service = DriverService(db)
    return service.update_location(
        latitude=location.latitude,
        longitude=location.longitude,
        shipment_id=location.shipment_id,
        location_name=location.location_name
    )

