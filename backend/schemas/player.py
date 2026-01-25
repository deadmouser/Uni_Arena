from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class PlayerBase(BaseModel):
    jersey_number: Optional[int] = None
    position: Optional[str] = None
    date_of_birth: Optional[date] = None


class PlayerCreate(PlayerBase):
    user_id: int
    team_id: Optional[int] = None


class PlayerResponse(PlayerBase):
    id: int
    user_id: int
    team_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
