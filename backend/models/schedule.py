from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum, Text, Boolean
from sqlalchemy.orm import relationship
import enum
from models.base import BaseModel


class ScheduleType(str, enum.Enum):
    ROUND_ROBIN = "round_robin"
    KNOCKOUT = "knockout"
    LEAGUE = "league"
    CUSTOM = "custom"


class Schedule(BaseModel):
    __tablename__ = "schedules"
    
    name = Column(String, nullable=False)  # e.g., "Football Tournament 2024"
    schedule_type = Column(Enum(ScheduleType), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    
    # Foreign keys
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=True)
    
    # Relationships
    sport = relationship("Sport", back_populates="schedules")
    tournament = relationship("Tournament", back_populates="schedules")
    matches = relationship("Match", back_populates="schedule")
