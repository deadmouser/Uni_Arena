from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.notification import NotificationType


class NotificationBase(BaseModel):
    title: str
    message: str
    notification_type: NotificationType
    link_url: Optional[str] = None


class NotificationCreate(NotificationBase):
    user_id: int


class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
