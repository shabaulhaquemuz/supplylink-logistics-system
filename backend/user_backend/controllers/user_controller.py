# ================================================================
# FILE: user_backend/controllers/user_controller.py
# ================================================================
"""
User Controller - Handles HTTP requests for user operations
"""
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.shared.database import get_db
from backend.shared.models import User
from backend.user_backend.services.user_service import UserService
from backend.user_backend.schemas.user_schema import UserRegister, UserResponse, Token
from backend.user_backend.dependencies import get_current_user


class UserController:
    def __init__(self, user_service: UserService):
        self.router = APIRouter(prefix="", tags=["Users"])
        self.user_service = user_service
        self._register_routes()

    def _register_routes(self):
        """Register all user routes"""
        self.router.add_api_route(
            "/register",
            self.register_user,
            methods=["POST"],
            response_model=UserResponse,
            status_code=status.HTTP_201_CREATED
        )
        self.router.add_api_route(
            "/token",
            self.login,
            methods=["POST"],
            response_model=Token
        )
        self.router.add_api_route(
            "/me",
            self.get_current_user_info,
            methods=["GET"],
            response_model=UserResponse
        )

    async def register_user(self, user_data: UserRegister, db: Session = Depends(get_db)):
        """Register a new customer"""
        return self.user_service.register_user(user_data, db)

    async def login(self, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
        """Login and get access token"""
        return self.user_service.login_user(form_data.username, form_data.password, db)

    async def get_current_user_info(self, current_user: User = Depends(get_current_user)):
        """Get current user information"""
        return current_user
