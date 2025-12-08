# ================================================================
# FILE: user_backend/services/user_service.py
# ================================================================
"""
User Service - Handles all user-related business logic
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt

from backend.shared.models import User, UserRole
from backend.user_backend.schemas.user_schema import UserRegister


class UserService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.SECRET_KEY = "your-secret-key-change-this-in-production"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def hash_password(self, password: str) -> str:
        """Hash a plain text password"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
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

    def register_user(self, user_data: UserRegister, db: Session) -> User:
        """Register a new customer"""
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        new_user = User(
            email=user_data.email,
            password_hash=self.hash_password(user_data.password),
            full_name=user_data.full_name,
            phone=user_data.phone,
            role=UserRole.CUSTOMER,
            is_active=True
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    def authenticate_user(self, email: str, password: str, db: Session) -> User:
        """Authenticate user and return user object"""
        user = db.query(User).filter(User.email == email).first()

        if not user or not self.verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user.role != UserRole.CUSTOMER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Customer accounts only."
            )

        return user

    def get_user_by_email(self, email: str, db: Session) -> User:
        """Get user by email"""
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def login_user(self, email: str, password: str, db: Session) -> dict:
        """Login user and return access token"""
        user = self.authenticate_user(email, password, db)

        access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}