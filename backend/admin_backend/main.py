# ================================================================
# FILE: admin_backend/main.py
# ================================================================
"""
Admin Backend - Main Application
Handles admin operations: shipment management, driver management, system oversight
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.shared.database import engine
from backend.shared.models import Base
from backend.admin_backend.services.admin_auth_service import AdminAuthService
from backend.admin_backend.services.admin_shipment_service import AdminShipmentService
from backend.admin_backend.services.admin_driver_service import AdminDriverService
from backend.admin_backend.controllers.admin_auth_controller import AdminAuthController
from backend.admin_backend.controllers.admin_shipment_controller import AdminShipmentController
from backend.admin_backend.controllers.admin_driver_controller import AdminDriverController

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Admin Backend API",
    version="1.0.0",
    description="Admin portal for logistics system management"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
admin_auth_service = AdminAuthService()
admin_shipment_service = AdminShipmentService()
admin_driver_service = AdminDriverService()

# Initialize controllers
admin_auth_controller = AdminAuthController(admin_auth_service)
admin_shipment_controller = AdminShipmentController(admin_shipment_service)
admin_driver_controller = AdminDriverController(admin_driver_service)

# Register routers
app.include_router(admin_auth_controller.router)
app.include_router(admin_shipment_controller.router)
app.include_router(admin_driver_controller.router)


@app.get("/")
async def root():
    return {
        "message": "Admin Backend API",
        "version": "1.0.0",
        "status": "active",
        "portal": "admin"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)