from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TeamBase(BaseModel):
    name: str
    code: Optional[str] = None


class TeamCreate(TeamBase):
    institution_id: int
    sport_id: int


class TeamResponse(TeamBase):
    id: int
    institution_id: int
    sport_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
