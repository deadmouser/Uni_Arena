from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models.auth import UserRole


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.VIEWER
    institution_id: Optional[int] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    institution_id: Optional[int] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    is_verified: bool
    institution_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    email: Optional[str] = None
