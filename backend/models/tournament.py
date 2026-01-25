from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
import enum
from models.base import BaseModel


class TournamentStatus(str, enum.Enum):
    UPCOMING = "upcoming"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Tournament(BaseModel):
    __tablename__ = "tournaments"
    
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(TournamentStatus), default=TournamentStatus.UPCOMING, nullable=False)
    is_public = Column(Boolean, default=True)  # Public tournaments visible to viewers
    is_active = Column(Boolean, default=True)
    
    # Foreign keys
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    
    # Relationships
    institution = relationship("Institution", back_populates="tournaments")
    schedules = relationship("Schedule", back_populates="tournament")
    sports = relationship("TournamentSport", back_populates="tournament")


class TournamentSport(BaseModel):
    """Many-to-many relationship between tournaments and sports"""
    __tablename__ = "tournament_sports"
    
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False)
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)
    
    # Relationships
    tournament = relationship("Tournament", back_populates="sports")
    sport = relationship("Sport")
