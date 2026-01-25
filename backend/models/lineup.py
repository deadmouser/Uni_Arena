from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, Text
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Lineup(BaseModel):
    """Team line-up for a specific match"""
    __tablename__ = "lineups"
    
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    is_starting = Column(Boolean, default=True)  # Starting line-up or substitute
    notes = Column(Text, nullable=True)
    
    # Relationships
    match = relationship("Match", back_populates="lineups")
    team = relationship("Team", back_populates="lineups")
    players = relationship("LineupPlayer", back_populates="lineup", cascade="all, delete-orphan")


class LineupPlayer(BaseModel):
    """Players in a line-up"""
    __tablename__ = "lineup_players"
    
    lineup_id = Column(Integer, ForeignKey("lineups.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    position = Column(String, nullable=True)  # Position in this match
    is_starting = Column(Boolean, default=True)  # Starting player or substitute
    role = Column(String, nullable=True)  # Specific role/assignment
    
    # Relationships
    lineup = relationship("Lineup", back_populates="players")
    player = relationship("Player")
