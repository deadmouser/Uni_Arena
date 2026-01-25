from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Player(BaseModel):
    __tablename__ = "players"
    
    jersey_number = Column(Integer, nullable=True)
    position = Column(String, nullable=True)  # e.g., "Forward", "Goalkeeper", "Singles", "Doubles"
    is_active = Column(Boolean, default=True)
    date_of_birth = Column(Date, nullable=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)  # Can be null for individual sports
    
    # Relationships
    user = relationship("User", back_populates="player_profile")
    team = relationship("Team", back_populates="players")
    match_participations = relationship("MatchParticipation", back_populates="player")
    statistics = relationship("PlayerStatistics", back_populates="player", uselist=False)
