# ================================================================
# FILE: user_backend/controllers/shipment_controller.py
# ================================================================
"""
Shipment Controller - Handles HTTP requests for shipment operations
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from backend.shared.database import get_db
from backend.shared.models import User
from backend.user_backend.services.shipment_service import ShipmentService
from backend.user_backend.schemas.shipment_schema import (
    ShipmentCreate, ShipmentResponse, TrackingResponse
)
from backend.user_backend.dependencies import get_current_user


class ShipmentController:
    def __init__(self, shipment_service: ShipmentService):
        self.router = APIRouter(prefix="/shipments", tags=["Shipments"])
        self.shipment_service = shipment_service
        self._register_routes()

    def _register_routes(self):
        """Register all shipment routes"""
        self.router.add_api_route(
            "",
            self.create_shipment,
            methods=["POST"],
            response_model=ShipmentResponse,
            status_code=status.HTTP_201_CREATED
        )
        self.router.add_api_route(
            "",
            self.get_my_shipments,
            methods=["GET"],
            response_model=List[ShipmentResponse]
        )
        self.router.add_api_route(
            "/{shipment_id}",
            self.get_shipment,
            methods=["GET"],
            response_model=ShipmentResponse
        )
        self.router.add_api_route(
            "/{shipment_id}/tracking",
            self.get_shipment_tracking,
            methods=["GET"],
            response_model=List[TrackingResponse]
        )
        self.router.add_api_route(
            "/{shipment_id}",
            self.cancel_shipment,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def create_shipment(
        self,
        shipment_data: ShipmentCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        """Create a new shipment"""
        return self.shipment_service.create_shipment(shipment_data, current_user, db)

    async def get_my_shipments(
        self,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        """Get all shipments for current user"""
        return self.shipment_service.get_user_shipments(current_user.id, db)

    async def get_shipment(
        self,
        shipment_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        """Get specific shipment details"""
        return self.shipment_service.get_shipment_by_id(shipment_id, current_user.id, db)

    async def get_shipment_tracking(
        self,
        shipment_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        """Get real-time tracking data for a shipment"""
        return self.shipment_service.get_shipment_tracking(shipment_id, current_user.id, db)

    async def cancel_shipment(
        self,
        shipment_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        """Cancel a shipment (only if status is PENDING)"""
        self.shipment_service.cancel_shipment(shipment_id, current_user.id, db)
        return None