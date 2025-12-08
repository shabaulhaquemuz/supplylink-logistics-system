# ================================================================
# FILE: user_backend/main.py
# ================================================================
"""
User Backend - Main Application
Handles customer-facing operations: registration, login, shipment booking, tracking
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.shared.database import engine
from backend.shared.models import Base
from backend.user_backend.services.user_service import UserService
from backend.user_backend.services.shipment_service import ShipmentService
from backend.user_backend.controllers.user_controller import UserController
from backend.user_backend.controllers.shipment_controller import ShipmentController

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="User Backend API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
user_service = UserService()
shipment_service = ShipmentService()

# Initialize controllers
user_controller = UserController(user_service)
shipment_controller = ShipmentController(shipment_service)

# Register routers
app.include_router(user_controller.router)
app.include_router(shipment_controller.router)


@app.get("/")
async def root():
    return {
        "message": "User Backend API",
        "version": "1.0.0",
        "status": "active"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)