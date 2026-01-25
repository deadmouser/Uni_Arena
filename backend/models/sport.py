from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from models.base import BaseModel


class SportType(str, enum.Enum):
    INDIVIDUAL = "individual"  # e.g., Tennis, Badminton singles
    TEAM = "team"  # e.g., Football, Basketball, Cricket
    MIXED = "mixed"  # e.g., Badminton doubles, Tennis doubles


class Sport(BaseModel):
    __tablename__ = "sports"
    
    name = Column(String, nullable=False, index=True)  # e.g., "Football", "Basketball"
    code = Column(String, unique=True, index=True, nullable=False)  # e.g., "FOOTBALL", "BASKETBALL"
    sport_type = Column(Enum(SportType), nullable=False)
    description = Column(Text, nullable=True)
    max_players_per_team = Column(Integer, nullable=True)  # For team sports
    min_players_per_team = Column(Integer, nullable=True)  # For team sports
    is_active = Column(Boolean, default=True)
    
    # Configuration and Rules (JSON)
    rules = Column(Text, nullable=True)  # JSON list of rules
    match_config = Column(Text, nullable=True)  # JSON object for match configuration
    mandatory_rules = Column(Text, nullable=True)  # JSON list of mandatory rules
    
    # Foreign keys
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    institution = relationship("Institution", back_populates="sports")
    organizer = relationship("User", back_populates="organized_sports")
    teams = relationship("Team", back_populates="sport")
    matches = relationship("Match", back_populates="sport")
    schedules = relationship("Schedule", back_populates="sport")
