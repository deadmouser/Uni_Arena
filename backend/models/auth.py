from sqlalchemy import Column, String, Boolean, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship
import enum
from models.base import BaseModel


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    ORGANIZER = "organizer"
    PLAYER = "player"
    VIEWER = "viewer"
    COACH = "coach"


class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.VIEWER, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Foreign key to institution
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=True)
    
    # Relationships
    institution = relationship("Institution", back_populates="users")
    player_profile = relationship("Player", back_populates="user", uselist=False)
    created_matches = relationship("Match", back_populates="created_by_user", foreign_keys="Match.created_by")
    organized_sports = relationship("Sport", back_populates="organizer")
    coached_teams = relationship("Team", back_populates="coach")
    notifications = relationship("Notification", back_populates="user")
