from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from models.match import MatchStatus
from schemas.sport import SportResponse
from schemas.team import TeamResponse


class MatchBase(BaseModel):
    match_number: Optional[str] = None
    scheduled_time: datetime
    notes: Optional[str] = None


class MatchCreate(MatchBase):
    sport_id: int
    home_team_id: Optional[int] = None
    away_team_id: Optional[int] = None
    schedule_id: Optional[int] = None
    player_ids: Optional[List[int]] = None  # For individual sports


class MatchUpdate(BaseModel):
    scheduled_time: Optional[datetime] = None
    status: Optional[MatchStatus] = None
    notes: Optional[str] = None
    actual_start_time: Optional[datetime] = None
    actual_end_time: Optional[datetime] = None


class MatchResponse(MatchBase):
    id: int
    sport_id: int
    home_team_id: Optional[int] = None
    away_team_id: Optional[int] = None
    schedule_id: Optional[int] = None
    status: MatchStatus
    actual_start_time: Optional[datetime] = None
    actual_end_time: Optional[datetime] = None
    venue_name: Optional[str] = None
    venue_id: Optional[int] = None
    created_by: int
    created_at: datetime
    # Optional relationships (included when loaded)
    sport: Optional[SportResponse] = None
    home_team: Optional[TeamResponse] = None
    away_team: Optional[TeamResponse] = None
    
    class Config:
        from_attributes = True
