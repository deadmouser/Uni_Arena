from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from models.schedule import ScheduleType


class ScheduleBase(BaseModel):
    name: str
    schedule_type: ScheduleType
    start_date: datetime
    end_date: Optional[datetime] = None
    description: Optional[str] = None


class ScheduleCreate(ScheduleBase):
    sport_id: int
    team_ids: Optional[List[int]] = None  # Teams/players to schedule
    player_ids: Optional[List[int]] = None  # For individual sports


class ScheduleResponse(ScheduleBase):
    id: int
    sport_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
