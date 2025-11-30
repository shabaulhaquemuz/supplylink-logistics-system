"""
Database Models (Shared across all backends)
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.shared.database import Base
import enum

class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    DRIVER = "driver"
    ADMIN = "admin"

class ShipmentStatus(str, enum.Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    shipments = relationship("Shipment", back_populates="customer", foreign_keys="Shipment.customer_id")
    driver_shipments = relationship("Shipment", back_populates="driver", foreign_keys="Shipment.driver_id")

class Shipment(Base):
    __tablename__ = "shipments"
    
    id = Column(Integer, primary_key=True, index=True)
    shipment_number = Column(String(50), unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"))
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    pickup_location = Column(String(255), nullable=False)
    delivery_location = Column(String(255), nullable=False)
    cargo_type = Column(String(100))
    weight = Column(Float)
    dimensions = Column(String(100))
    
    status = Column(Enum(ShipmentStatus), default=ShipmentStatus.PENDING)
    estimated_delivery = Column(DateTime)
    actual_delivery = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("User", back_populates="shipments", foreign_keys=[customer_id])
    driver = relationship("User", back_populates="driver_shipments", foreign_keys=[driver_id])
    tracking = relationship("TrackingData", back_populates="shipment")

class TrackingData(Base):
    __tablename__ = "tracking_data"
    
    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"))
    latitude = Column(Float)
    longitude = Column(Float)
    location_name = Column(String(255))
    status_update = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    shipment = relationship("Shipment", back_populates="tracking")