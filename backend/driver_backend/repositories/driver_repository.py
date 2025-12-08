"""
Driver Repository - All driver DB operations
This file contains the repository layer for all driver-related database operations.

It provides a clean separation between business logic and raw SQL queries.

DriverRepository receives a SQLAlchemy session, enabling safe and reusable DB access.

get_driver_by_email() fetches a driver account while ensuring the role is strictly DRIVER.

get_driver_by_id() retrieves driver details using their unique database ID.

update_driver_status() allows enabling/disabling a driver (e.g., online/offline mode).

All methods return clean Python objects or None, making them easy to use in services.

In simple words — this file is the database helper used by services to read/update driver data without repeating query code.
"""
"""
Driver Repository - All driver DB operations
"""
from sqlalchemy.orm import Session
from backend.shared.models import User, UserRole
from typing import Optional
from backend.shared.utils import hash_password



class DriverRepository:
    """Handle all driver database operations"""

    def __init__(self, db: Session):
        self.db = db

    # -------------------- CREATE DRIVER --------------------
    def create_driver(self, full_name: str, email: str, phone: str, password: str) -> User:
        """Create new driver account"""

        # Check if email already exists
        existing = self.db.query(User).filter(User.email == email).first()
        if existing:
            return None

        new_driver = User(
            email=email,
            password_hash=hash_password(password),
            full_name=full_name,
            phone=phone,
            role="DRIVER"
        )

        self.db.add(new_driver)
        self.db.commit()
        self.db.refresh(new_driver)

        return new_driver

    # -------------------- GET DRIVER BY EMAIL --------------------
    def get_driver_by_email(self, email: str) -> Optional[User]:
        return (
            self.db.query(User)
            .filter(User.email == email, User.role == UserRole.DRIVER)
            .first()
        )

    # -------------------- GET DRIVER BY ID -----------------------
    def get_driver_by_id(self, driver_id: int) -> Optional[User]:
        return (
            self.db.query(User)
            .filter(User.id == driver_id, User.role == UserRole.DRIVER)
            .first()
        )

    # -------------------- UPDATE ACTIVE STATUS -------------------
    def update_driver_status(self, driver_id: int, is_active: bool) -> bool:
        driver = self.get_driver_by_id(driver_id)
        if driver:
            driver.is_active = is_active
            self.db.commit()
            return True
        return False

