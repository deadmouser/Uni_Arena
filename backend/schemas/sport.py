from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.sport import SportType


class SportBase(BaseModel):
    name: str
    code: str
    sport_type: SportType
    description: Optional[str] = None
    max_players_per_team: Optional[int] = None
    min_players_per_team: Optional[int] = None
    rules: Optional[str] = None  # JSON string
    match_config: Optional[str] = None  # JSON string
    mandatory_rules: Optional[str] = None  # JSON string


class SportCreate(SportBase):
    template_code: Optional[str] = None  # To create from template


class SportUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    max_players_per_team: Optional[int] = None
    min_players_per_team: Optional[int] = None
    is_active: Optional[bool] = None
    rules: Optional[str] = None
    match_config: Optional[str] = None
    mandatory_rules: Optional[str] = None


class SportResponse(SportBase):
    id: int
    institution_id: int
    organizer_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
