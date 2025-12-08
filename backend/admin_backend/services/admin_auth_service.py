# ================================================================
# FILE: admin_backend/services/admin_auth_service.py
# ================================================================
"""
Admin Authentication Service
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt

from backend.shared.models import User, UserRole


class AdminAuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.SECRET_KEY = "admin-secret-key-change-in-production"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 60

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def decode_token(self, token: str) -> str:
        """Decode JWT token and return email"""
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return email
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def authenticate_admin(self, email: str, password: str, db: Session) -> User:
        """Authenticate admin user"""
        user = db.query(User).filter(User.email == email).first()

        if not user or not self.verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check if user has ADMIN role
        if user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Admin accounts only."
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )

        return user

    def get_admin_by_email(self, email: str, db: Session) -> User:
        """Get admin user by email"""
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify ADMIN role
        if user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        return user

    def login_admin(self, email: str, password: str, db: Session) -> dict:
        """Login admin and return access token"""
        admin = self.authenticate_admin(email, password, db)

        access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": admin.email}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
