# ================================================================
# FILE: user_backend/schemas/user_schema.py
# ================================================================
"""
User-related Pydantic schemas
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    phone: Optional[str]
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True