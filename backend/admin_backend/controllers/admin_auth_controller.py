# ================================================================
# FILE: admin_backend/controllers/admin_auth_controller.py
# ================================================================
"""
Admin Authentication Controller
"""
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.shared.database import get_db
from backend.shared.models import User
from backend.admin_backend.services.admin_auth_service import AdminAuthService
from backend.admin_backend.schemas.admin_auth_schema import AdminLogin, AdminToken, AdminResponse
from backend.admin_backend.dependencies import get_current_admin


class AdminAuthController:
    def __init__(self, admin_auth_service: AdminAuthService):
        self.router = APIRouter(prefix="/admin", tags=["Admin Authentication"])
        self.admin_auth_service = admin_auth_service
        self._register_routes()

    def _register_routes(self):
        """Register authentication routes"""
        self.router.add_api_route(
            "/token",
            self.login,
            methods=["POST"],
            response_model=AdminToken
        )
        self.router.add_api_route(
            "/me",
            self.get_current_admin_info,
            methods=["GET"],
            response_model=AdminResponse
        )

    async def login(
        self,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
    ):
        """Admin login and get access token"""
        return self.admin_auth_service.login_admin(form_data.username, form_data.password, db)

    async def get_current_admin_info(
        self,
        current_admin: User = Depends(get_current_admin)
    ):
        """Get current admin information"""
        return current_admin