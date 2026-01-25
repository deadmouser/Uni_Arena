from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class LineupPlayerBase(BaseModel):
    player_id: int
    position: Optional[str] = None
    is_starting: bool = True
    role: Optional[str] = None


class LineupBase(BaseModel):
    match_id: int
    team_id: int
    is_starting: bool = True
    notes: Optional[str] = None


class LineupCreate(LineupBase):
    players: List[LineupPlayerBase]


class LineupResponse(LineupBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class LineupPlayerResponse(LineupPlayerBase):
    id: int
    lineup_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
