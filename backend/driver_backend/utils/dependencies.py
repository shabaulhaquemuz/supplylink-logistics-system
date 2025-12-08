"""
FastAPI Dependencies
This file contains FastAPI dependency functions, which help secure driver routes using JWT tokens.

It uses HTTPBearer to extract the Authorization: Bearer <token> header from incoming requests.

get_current_driver() verifies the token using the shared JWT utility.

If the token is invalid or expired, it raises a 401 Unauthorized error.

It also checks whether the token belongs to a driver; otherwise it returns a 403 Forbidden.

The database session is injected automatically using Depends(get_db).

Successful validation returns the JWT payload containing driver ID, email, and role.

In simple words — this file is the security gatekeeper that ensures only logged-in drivers can access protected APIs.
"""
"""
Dependencies and utilities for Driver Backend
"""
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.shared.database import get_db
from backend.shared.utils import verify_token
from typing import Dict

# Load environment variables
load_dotenv()

# Get OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Security
security = HTTPBearer()

async def get_current_driver(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Verify JWT token and return current driver info
    """
    token = credentials.credentials
    
    try:
        payload = verify_token(token)
        driver_id = payload.get("user_id")
        
        if not driver_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )
        
        return {
            "driver_id": driver_id,
            "email": payload.get("email"),
            "role": payload.get("role")
        }
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )