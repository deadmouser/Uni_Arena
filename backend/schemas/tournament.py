from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from models.tournament import TournamentStatus


class TournamentBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    is_public: bool = True


class TournamentCreate(TournamentBase):
    institution_id: int
    sport_ids: Optional[List[int]] = None


class TournamentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[TournamentStatus] = None
    is_public: Optional[bool] = None


class TournamentResponse(TournamentBase):
    id: int
    institution_id: int
    status: TournamentStatus
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
