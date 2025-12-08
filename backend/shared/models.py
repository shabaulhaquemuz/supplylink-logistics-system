"""
Database Models (Shared across all backends)
CLEAN VERSION WITH CLEAR USER + DRIVER SEPARATION
"""
import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Enum,
    ForeignKey, Text, Boolean
)
from sqlalchemy.orm import relationship
from backend.shared.database import Base
from backend.driver_backend.utils.enums import (
    ShipmentType, InternationalMode, CustomsStatus,
    CODStatus, FailureReason, DelayReason, PortLocation,
    ShipmentStatus
)



# ================================================================
# --------------- USER + DRIVER + ADMIN ENUMS --------------------
# ================================================================
class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    DRIVER = "driver"
    ADMIN = "admin"




# ================================================================
# ======================= USER MODEL =============================
# (Everything below is related to USER functionality)
# A user can be CUSTOMER or DRIVER based on role.
# ================================================================
class User(Base):
    __tablename__ = "users"

    # ---------------- USER BASIC DETAILS ----------------
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)

    # ------------------- TIMESTAMPS ----------------------
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ------------------- RELATIONSHIPS -------------------
    # USER (Customer) → Shipment (1-to-many)
    shipments = relationship(
        "Shipment",
        back_populates="customer",
        foreign_keys="Shipment.customer_id"
    )

    # DRIVER → Shipment they are assigned to
    driver_shipments = relationship(
        "Shipment",
        back_populates="driver",
        foreign_keys="Shipment.driver_id"
    )



# ================================================================
# ======================= SHIPMENT MODEL =========================
# This model is SHARED by USER + DRIVER
# USER creates a shipment
# DRIVER updates progress, tracking, pickup, delivery, etc.
# ================================================================
class Shipment(Base):
    __tablename__ = "shipments"



    # ============================================================
    # -------------------- USER PART STARTS -----------------------
    # ============================================================

    # These fields come from USER when booking a shipment.
    id = Column(Integer, primary_key=True, index=True)
    shipment_number = Column(String(50), unique=True, index=True)

    customer_id = Column(Integer, ForeignKey("users.id"))
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



    # ============================================================
    # -------------------- DRIVER PART STARTS ---------------------
    # ============================================================

    # DRIVER assigned to the shipment
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=True)



    # ----------------- INTERNATIONAL LOGISTICS ------------------
    # These fields are used when shipment is international and 
    # driver handles customs + international movement.
    shipment_type = Column(Enum(ShipmentType), default=ShipmentType.DOMESTIC)
    international_mode = Column(Enum(InternationalMode), nullable=True)
    port_of_entry = Column(Enum(PortLocation), nullable=True)
    customs_clearance_status = Column(Enum(CustomsStatus), nullable=True)
    customs_cleared_at = Column(DateTime, nullable=True)



    # --------------------------- COD -----------------------------
    # Driver collects COD amount; user sees COD in their shipment.
    is_cod = Column(Boolean, default=False)
    cod_amount = Column(Float, nullable=True)
    cod_status = Column(Enum(CODStatus), default=CODStatus.NOT_APPLICABLE)
    cod_collected_at = Column(DateTime, nullable=True)



    # ----------------------- PICKUP ACTIONS ----------------------
    # Driver marks pickup as completed
    is_home_pickup = Column(Boolean, default=False)
    pickup_completed_at = Column(DateTime, nullable=True)



    # ----------------------- DELIVERY ACTIONS --------------------
    # Driver attempts and completes delivery
    is_home_delivery = Column(Boolean, default=True)
    delivery_attempted_at = Column(DateTime, nullable=True)



    # --------------------- FAILURE TRACKING ----------------------
    # When driver fails delivery, they specify reason + notes
    failure_reason = Column(Enum(FailureReason), nullable=True)
    failure_notes = Column(Text, nullable=True)



    # ----------------------- DELAY TRACKING ----------------------
    # Driver can report delays (traffic, vehicle issue, etc.)
    delay_reason = Column(Enum(DelayReason), nullable=True)
    delay_reported_at = Column(DateTime, nullable=True)
    delay_notes = Column(Text, nullable=True)



    # ---------------------- PRICING ENGINE -----------------------
    # System calculates price; user sees it in their app
    base_price = Column(Float, nullable=True)
    fuel_surcharge = Column(Float, nullable=True)
    total_price = Column(Float, nullable=True)



    # ----------------------- RELATIONSHIPS -----------------------
    customer = relationship("User", back_populates="shipments", foreign_keys=[customer_id])
    driver = relationship("User", back_populates="driver_shipments", foreign_keys=[driver_id])
    tracking = relationship("TrackingData", back_populates="shipment")



# ================================================================
# ===================== TRACKING MODEL ===========================
# DRIVER updates real-time location.
# USER views real-time tracking.
# ================================================================
class TrackingData(Base):
    __tablename__ = "tracking_data"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"))

    latitude = Column(Float)
    longitude = Column(Float)
    location_name = Column(String(255))
    status_update = Column(String(255))

    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship
    shipment = relationship("Shipment", back_populates="tracking")