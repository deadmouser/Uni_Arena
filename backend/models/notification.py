from sqlalchemy import Column, String, Text, Integer, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
from models.base import BaseModel


class NotificationType(str, enum.Enum):
    MATCH_SCHEDULED = "match_scheduled"
    MATCH_REMINDER = "match_reminder"
    SCORE_UPDATE = "score_update"
    TEAM_JOIN = "team_join"
    LINEUP_CHANGE = "lineup_change"
    TOURNAMENT_UPDATE = "tournament_update"
    GENERAL = "general"


class Notification(BaseModel):
    __tablename__ = "notifications"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime(timezone=True), nullable=True)
    link_url = Column(String, nullable=True)  # Link to related resource
    
    # Relationships
    user = relationship("User", back_populates="notifications")
