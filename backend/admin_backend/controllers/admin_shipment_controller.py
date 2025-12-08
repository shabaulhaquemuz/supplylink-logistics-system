
# ================================================================
# FILE: admin_backend/controllers/admin_shipment_controller.py
# ================================================================
"""
Admin Shipment Management Controller
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from backend.shared.database import get_db
from backend.shared.models import User
from backend.admin_backend.services.admin_shipment_service import AdminShipmentService
from backend.admin_backend.schemas.admin_shipment_schema import (
    ShipmentListResponse, AssignDriverRequest, UpdateShipmentStatusRequest
)
from backend.admin_backend.dependencies import get_current_admin


class AdminShipmentController:
    def __init__(self, admin_shipment_service: AdminShipmentService):
        self.router = APIRouter(prefix="/admin/shipments", tags=["Admin Shipment Management"])
        self.admin_shipment_service = admin_shipment_service
        self._register_routes()

    def _register_routes(self):
        """Register shipment management routes"""
        self.router.add_api_route(
            "",
            self.get_all_shipments,
            methods=["GET"],
            response_model=List[ShipmentListResponse]
        )
        self.router.add_api_route(
            "/{shipment_id}",
            self.get_shipment,
            methods=["GET"],
            response_model=ShipmentListResponse
        )
        self.router.add_api_route(
            "/{shipment_id}/assign-driver",
            self.assign_driver,
            methods=["POST"],
            response_model=ShipmentListResponse
        )
        self.router.add_api_route(
            "/{shipment_id}/status",
            self.update_status,
            methods=["PUT"],
            response_model=ShipmentListResponse
        )

    async def get_all_shipments(
        self,
        current_admin: User = Depends(get_current_admin),
        db: Session = Depends(get_db)
    ):
        """Get all shipments"""
        return self.admin_shipment_service.get_all_shipments(db)

    async def get_shipment(
        self,
        shipment_id: int,
        current_admin: User = Depends(get_current_admin),
        db: Session = Depends(get_db)
    ):
        """Get specific shipment"""
        return self.admin_shipment_service.get_shipment_by_id(shipment_id, db)

    async def assign_driver(
        self,
        shipment_id: int,
        request: AssignDriverRequest,
        current_admin: User = Depends(get_current_admin),
        db: Session = Depends(get_db)
    ):
        """Assign driver to shipment"""
        return self.admin_shipment_service.assign_driver_to_shipment(
            shipment_id, request.driver_id, db
        )

    async def update_status(
        self,
        shipment_id: int,
        request: UpdateShipmentStatusRequest,
        current_admin: User = Depends(get_current_admin),
        db: Session = Depends(get_db)
    ):
        """Update shipment status"""
        return self.admin_shipment_service.update_shipment_status(
            shipment_id, request.status, db
        )