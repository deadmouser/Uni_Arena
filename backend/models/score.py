from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Text
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Score(BaseModel):
    """Current score for a match"""
    __tablename__ = "scores"
    
    match_id = Column(Integer, ForeignKey("matches.id"), unique=True, nullable=False)
    home_score = Column(Integer, default=0, nullable=False)
    away_score = Column(Integer, default=0, nullable=False)
    period = Column(String, nullable=True)  # e.g., "1st Half", "2nd Set", "Quarter 1"
    additional_info = Column(Text, nullable=True)  # JSON string for sport-specific data
    
    # Relationships
    match = relationship("Match", back_populates="scores")


class ScoreUpdate(BaseModel):
    """History of score updates for live tracking"""
    __tablename__ = "score_updates"
    
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    home_score = Column(Integer, default=0, nullable=False)
    away_score = Column(Integer, default=0, nullable=False)
    period = Column(String, nullable=True)
    update_type = Column(String, nullable=True)  # e.g., "goal", "point", "foul"
    description = Column(Text, nullable=True)  # e.g., "Goal by Player X"
    updated_at = Column(DateTime(timezone=True), nullable=False)
    
    # Relationships
    match = relationship("Match", back_populates="score_updates")
