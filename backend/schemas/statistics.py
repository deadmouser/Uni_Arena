from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PlayerStatisticsResponse(BaseModel):
    id: int
    player_id: int
    matches_played: int
    matches_won: int
    matches_lost: int
    matches_drawn: int
    sport_specific_stats: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TeamStatisticsResponse(BaseModel):
    id: int
    team_id: int
    matches_played: int
    matches_won: int
    matches_lost: int
    matches_drawn: int
    goals_for: int
    goals_against: int
    sport_specific_stats: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
