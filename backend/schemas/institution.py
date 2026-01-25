from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InstitutionBase(BaseModel):
    name: str
    code: str
    address: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    description: Optional[str] = None


class InstitutionCreate(InstitutionBase):
    code: Optional[str] = None


class InstitutionUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    address: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None


class InstitutionResponse(InstitutionBase):
    id: int
    logo_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
