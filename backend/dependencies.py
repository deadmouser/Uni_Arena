from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models.auth import User
from security.auth_service import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login", auto_error=False)
oauth2_scheme_required = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get the current authenticated user (optional - returns None if not authenticated)"""
    if not token:
        return None
    
    payload = decode_access_token(token)
    if payload is None:
        return None
    
    email: str = payload.get("sub")
    if email is None:
        return None
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        return None
    
    if not user.is_active:
        return None
    
    return user


async def get_current_user_required(
    token: str = Depends(oauth2_scheme_required),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user (required - raises exception if not authenticated)"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user
