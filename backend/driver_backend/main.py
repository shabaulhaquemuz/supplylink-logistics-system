"""
Driver Backend - FastAPI Application
Production-grade OOP architecture
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.shared.database import engine, Base  # REVERT: add 'backend.' back
from backend.shared.config import settings  # REVERT: add 'backend.' back
from backend.driver_backend.controllers import (  # REVERT: add 'backend.' back
    driver_controller,
    shipment_controller,
    pricing_controller,
    voice_controller  # JUST ADD THIS LINE
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Logistics - Driver Backend",
    description="Driver operations, shipment tracking, and delivery management",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    driver_controller.router,
    prefix="/api/driver",
    tags=["Driver Operations"]
)

app.include_router(
    shipment_controller.router,
    prefix="/api/driver",
    tags=["Shipment Management"]
)

app.include_router(
    pricing_controller.router,
    prefix="/api/driver",
    tags=["Pricing"]
)

app.include_router(
    voice_controller.router,
    prefix="/api/driver",
    tags=["Voice Assistant"]
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Driver Backend API - OOP Architecture",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
        "features": ["Voice Assistant", "Shipment Tracking", "Pricing"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "service": "driver_backend",
        "ai_features": "enabled"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT_DRIVER,
        reload=True
    )