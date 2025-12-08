# ================================================================
# FILE: admin_backend/services/admin_driver_service.py
# ================================================================
"""
Admin Driver Management Service
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from backend.shared.models import User, UserRole


class AdminDriverService:
    def __init__(self):
        pass

    def get_all_drivers(self, db: Session) -> List[User]:
        """Get all drivers in the system"""
        drivers = db.query(User).filter(
            User.role == UserRole.DRIVER
        ).order_by(User.created_at.desc()).all()
        
        return drivers

    def get_driver_by_id(self, driver_id: int, db: Session) -> User:
        """Get specific driver by ID"""
        driver = db.query(User).filter(
            User.id == driver_id,
            User.role == UserRole.DRIVER
        ).first()

        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )

        return driver

    def update_driver_status(self, driver_id: int, is_active: bool, db: Session) -> User:
        """Activate or deactivate a driver"""
        driver = self.get_driver_by_id(driver_id, db)

        driver.is_active = is_active

        db.commit()
        db.refresh(driver)

        return driver

    def approve_driver(self, driver_id: int, db: Session) -> User:
        """Approve/activate a driver"""
        return self.update_driver_status(driver_id, True, db)

    def deactivate_driver(self, driver_id: int, db: Session) -> User:
        """Deactivate a driver"""
        return self.update_driver_status(driver_id, False, db)