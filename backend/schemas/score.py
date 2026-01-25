from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ScoreBase(BaseModel):
    home_score: int = 0
    away_score: int = 0
    period: Optional[str] = None
    additional_info: Optional[str] = None


class ScoreUpdate(BaseModel):
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    period: Optional[str] = None
    update_type: Optional[str] = None
    description: Optional[str] = None
    additional_info: Optional[str] = None
    # Sport-specific fields
    action: Optional[str] = None  # e.g., "add_run", "wicket", "goal", "point", etc.
    points: Optional[int] = None  # For basketball/cricket runs
    player_id: Optional[int] = None  # Player involved in action
    team: Optional[str] = None  # "home" or "away"
    sport_specific_data: Optional[Dict[str, Any]] = None  # Additional sport-specific data


class ScoreResponse(ScoreBase):
    id: int
    match_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
