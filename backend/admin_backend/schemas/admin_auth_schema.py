# ================================================================
# FILE: admin_backend/schemas/admin_auth_schema.py
# ================================================================
"""
Admin Authentication Schemas
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class AdminToken(BaseModel):
    access_token: str
    token_type: str


class AdminResponse(BaseModel):
    id: int
    email: str
    full_name: str
    phone: Optional[str]
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
