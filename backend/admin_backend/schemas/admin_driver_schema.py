# ================================================================
# FILE: admin_backend/schemas/admin_driver_schema.py
# ================================================================
"""
Admin Driver Management Schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DriverResponse(BaseModel):
    id: int
    email: str
    full_name: str
    phone: Optional[str]
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DriverStatusUpdate(BaseModel):
    is_active: bool