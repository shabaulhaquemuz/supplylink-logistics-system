# ================================================================
# FILE: admin_backend/controllers/admin_driver_controller.py
# ================================================================
"""
Admin Driver Management Controller
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from backend.shared.database import get_db
from backend.shared.models import User
from backend.admin_backend.services.admin_driver_service import AdminDriverService
from backend.admin_backend.schemas.admin_driver_schema import DriverResponse, DriverStatusUpdate
from backend.admin_backend.dependencies import get_current_admin


class AdminDriverController:
    def __init__(self, admin_driver_service: AdminDriverService):
        self.router = APIRouter(prefix="/admin/drivers", tags=["Admin Driver Management"])
        self.admin_driver_service = admin_driver_service
        self._register_routes()

    def _register_routes(self):
        """Register driver management routes"""
        self.router.add_api_route(
            "",
            self.get_all_drivers,
            methods=["GET"],
            response_model=List[DriverResponse]
        )
        self.router.add_api_route(
            "/{driver_id}",
            self.get_driver,
            methods=["GET"],
            response_model=DriverResponse
        )
        self.router.add_api_route(
            "/{driver_id}/status",
            self.update_driver_status,
            methods=["PUT"],
            response_model=DriverResponse
        )
        self.router.add_api_route(
            "/{driver_id}/approve",
            self.approve_driver,
            methods=["POST"],
            response_model=DriverResponse
        )
        self.router.add_api_route(
            "/{driver_id}/deactivate",
            self.deactivate_driver,
            methods=["POST"],
            response_model=DriverResponse
        )

    async def get_all_drivers(
        self,
        current_admin: User = Depends(get_current_admin),
        db: Session = Depends(get_db)
    ):
        """Get all drivers"""
        return self.admin_driver_service.get_all_drivers(db)

    async def get_driver(
        self,
        driver_id: int,
        current_admin: User = Depends(get_current_admin),
        db: Session = Depends(get_db)
    ):
        """Get specific driver"""
        return self.admin_driver_service.get_driver_by_id(driver_id, db)

    async def update_driver_status(
        self,
        driver_id: int,
        request: DriverStatusUpdate,
        current_admin: User = Depends(get_current_admin),
        db: Session = Depends(get_db)
    ):
        """Update driver status"""
        return self.admin_driver_service.update_driver_status(driver_id, request.is_active, db)

    async def approve_driver(
        self,
        driver_id: int,
        current_admin: User = Depends(get_current_admin),
        db: Session = Depends(get_db)
    ):
        """Approve/activate driver"""
        return self.admin_driver_service.approve_driver(driver_id, db)

    async def deactivate_driver(
        self,
        driver_id: int,
        current_admin: User = Depends(get_current_admin),
        db: Session = Depends(get_db)
    ):
        """Deactivate driver"""
        return self.admin_driver_service.deactivate_driver(driver_id, db)
