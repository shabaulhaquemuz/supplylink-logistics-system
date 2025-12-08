# ================================================================
# FILE: admin_backend/dependencies.py
# ================================================================
"""
Admin Dependency Injection
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.shared.database import get_db
from backend.shared.models import User
from backend.admin_backend.services.admin_auth_service import AdminAuthService

# Bearer token authentication scheme
security = HTTPBearer()

# Initialize admin auth service
admin_auth_service = AdminAuthService()


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Dependency to get current authenticated admin"""
    token = credentials.credentials
    email = admin_auth_service.decode_token(token)
    return admin_auth_service.get_admin_by_email(email, db)
