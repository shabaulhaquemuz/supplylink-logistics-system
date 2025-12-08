# ================================================================
# FILE: user_backend/dependencies.py
# ================================================================
"""
Dependency injection for authentication
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.shared.database import get_db
from backend.shared.models import User
from backend.user_backend.services.user_service import UserService

# Bearer token authentication scheme
security = HTTPBearer()

# Initialize user service
user_service = UserService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    email = user_service.decode_token(token)
    return user_service.get_user_by_email(email, db)
