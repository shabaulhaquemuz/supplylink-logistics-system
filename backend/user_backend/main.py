"""
User Backend API
Handles customer registration, login, and shipment booking
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from backend.shared.database import get_db, engine, Base
from backend.shared.models import User, Shipment, UserRole, ShipmentStatus
from backend.shared.utils import hash_password, verify_password, create_access_token
from backend.shared.config import settings

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Logistics - User API",
    description="Customer registration, login, and shipment management",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ShipmentCreate(BaseModel):
    pickup_location: str
    delivery_location: str
    cargo_type: str
    weight: float
    dimensions: str

# Routes
@app.get("/")
async def root():
    return {"message": "User Backend API", "status": "running"}

@app.post("/api/user/register")
async def register(user: UserRegister, db: Session = Depends(get_db)):
    """Register new customer"""
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        full_name=user.full_name,
        phone=user.phone,
        role=UserRole.CUSTOMER
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully", "user_id": new_user.id}

@app.post("/api/user/login")
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Customer login"""
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if user.role != UserRole.CUSTOMER:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Create token
    token = create_access_token(data={"sub": user.email, "role": user.role.value})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.value
        }
    }

@app.post("/api/user/shipments")
async def create_shipment(shipment: ShipmentCreate, db: Session = Depends(get_db)):
    """Create new shipment (simplified - add auth later)"""
    import random
    
    new_shipment = Shipment(
        shipment_number=f"SHP{random.randint(10000, 99999)}",
        customer_id=1,  # TODO: Get from JWT token
        pickup_location=shipment.pickup_location,
        delivery_location=shipment.delivery_location,
        cargo_type=shipment.cargo_type,
        weight=shipment.weight,
        dimensions=shipment.dimensions,
        status=ShipmentStatus.PENDING
    )
    db.add(new_shipment)
    db.commit()
    db.refresh(new_shipment)
    
    return {
        "message": "Shipment created successfully",
        "shipment_number": new_shipment.shipment_number,
        "status": new_shipment.status.value
    }

@app.get("/api/user/shipments/{shipment_id}")
async def get_shipment(shipment_id: int, db: Session = Depends(get_db)):
    """Get shipment details"""
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
    return {
        "id": shipment.id,
        "shipment_number": shipment.shipment_number,
        "pickup_location": shipment.pickup_location,
        "delivery_location": shipment.delivery_location,
        "status": shipment.status.value,
        "created_at": shipment.created_at
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.API_PORT_USER, reload=True)