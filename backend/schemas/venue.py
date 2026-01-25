from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VenueBase(BaseModel):
    name: str
    address: Optional[str] = None
    capacity: Optional[int] = None
    facilities: Optional[str] = None


class VenueCreate(VenueBase):
    institution_id: int


class VenueResponse(VenueBase):
    id: int
    institution_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
