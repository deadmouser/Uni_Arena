from sqlalchemy import Column, Integer, ForeignKey, Float, String, Text
from sqlalchemy.orm import relationship
from models.base import BaseModel


class PlayerStatistics(BaseModel):
    """Player performance statistics"""
    __tablename__ = "player_statistics"
    
    player_id = Column(Integer, ForeignKey("players.id"), unique=True, nullable=False)
    
    # Match statistics
    matches_played = Column(Integer, default=0)
    matches_won = Column(Integer, default=0)
    matches_lost = Column(Integer, default=0)
    matches_drawn = Column(Integer, default=0)
    
    # Sport-specific statistics (stored as JSON string)
    sport_specific_stats = Column(Text, nullable=True)  # JSON string for flexible stats
    
    # Relationships
    player = relationship("Player", uselist=False)


class TeamStatistics(BaseModel):
    """Team performance statistics"""
    __tablename__ = "team_statistics"
    
    team_id = Column(Integer, ForeignKey("teams.id"), unique=True, nullable=False)
    
    # Match statistics
    matches_played = Column(Integer, default=0)
    matches_won = Column(Integer, default=0)
    matches_lost = Column(Integer, default=0)
    matches_drawn = Column(Integer, default=0)
    
    # Goals/Points (sport-agnostic)
    goals_for = Column(Integer, default=0)
    goals_against = Column(Integer, default=0)
    
    # Sport-specific statistics
    sport_specific_stats = Column(Text, nullable=True)  # JSON string
    
    # Relationships
    team = relationship("Team", uselist=False)
