from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum, Text, Boolean
from sqlalchemy.orm import relationship
import enum
from models.base import BaseModel


class MatchStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    LIVE = "live"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    POSTPONED = "postponed"


class Match(BaseModel):
    __tablename__ = "matches"
    
    match_number = Column(String, nullable=True, index=True)  # e.g., "M001", "QF-1"
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    actual_start_time = Column(DateTime(timezone=True), nullable=True)
    actual_end_time = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(MatchStatus), default=MatchStatus.SCHEDULED, nullable=False)
    venue_name = Column(String, nullable=True)  # Legacy field, use venue_id instead
    notes = Column(Text, nullable=True)
    
    # Foreign keys
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)  # Null for individual sports
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)  # Null for individual sports
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    sport = relationship("Sport", back_populates="matches")
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    schedule = relationship("Schedule", back_populates="matches")
    venue = relationship("Venue", back_populates="matches")
    created_by_user = relationship("User", foreign_keys=[created_by], back_populates="created_matches")
    participations = relationship("MatchParticipation", back_populates="match", cascade="all, delete-orphan")
    scores = relationship("Score", back_populates="match", cascade="all, delete-orphan")
    score_updates = relationship("ScoreUpdate", back_populates="match", cascade="all, delete-orphan")
    lineups = relationship("Lineup", back_populates="match", cascade="all, delete-orphan")


class MatchParticipation(BaseModel):
    """For individual sports or tracking specific players in team sports"""
    __tablename__ = "match_participations"
    
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    is_home = Column(Boolean, default=True)  # True for home/player1, False for away/player2
    
    # Relationships
    match = relationship("Match", back_populates="participations")
    player = relationship("Player", back_populates="match_participations")
