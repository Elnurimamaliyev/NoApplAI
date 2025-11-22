from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.notification import NotificationType


class NotificationCreate(BaseModel):
    user_id: int
    type: NotificationType
    title: str
    message: str
    application_id: Optional[int] = None
    program_id: Optional[int] = None


class NotificationUpdate(BaseModel):
    is_read: bool


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    type: NotificationType
    title: str
    message: str
    is_read: bool
    application_id: Optional[int] = None
    program_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
