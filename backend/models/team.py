from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Team(BaseModel):
    __tablename__ = "teams"
    
    name = Column(String, nullable=False, index=True)
    code = Column(String, nullable=True)  # Team code/abbreviation
    is_active = Column(Boolean, default=True)
    
    # Foreign keys
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)
    coach_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Coach assigned to team
    
    # Relationships
    institution = relationship("Institution", back_populates="teams")
    sport = relationship("Sport", back_populates="teams")
    coach = relationship("User", foreign_keys=[coach_id], back_populates="coached_teams")
    players = relationship("Player", back_populates="team")
    home_matches = relationship("Match", foreign_keys="Match.home_team_id", back_populates="home_team")
    away_matches = relationship("Match", foreign_keys="Match.away_team_id", back_populates="away_team")
    lineups = relationship("Lineup", back_populates="team")
    statistics = relationship("TeamStatistics", back_populates="team", uselist=False)
