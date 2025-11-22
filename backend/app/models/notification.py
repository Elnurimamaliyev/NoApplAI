"""
Notification model
"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class NotificationType(str, enum.Enum):
    DEADLINE = "deadline"
    AI_MATCH = "ai_match"
    DOCUMENT = "document"
    OFFER = "offer"
    STATUS_UPDATE = "status_update"
    REMINDER = "reminder"
    SYSTEM = "system"


class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Notification content
    notification_type = Column(SQLEnum(NotificationType), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    
    # Status
    is_read = Column(Boolean, default=False, index=True)
    is_deleted = Column(Boolean, default=False)
    
    # Optional: Link to related entities
    related_application_id = Column(String, ForeignKey("applications.id", ondelete="SET NULL"), nullable=True)
    related_program_id = Column(String, ForeignKey("programs.id", ondelete="SET NULL"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    read_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification {self.title} - Read: {self.is_read}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "notification_type": self.notification_type.value if self.notification_type else None,
            "title": self.title,
            "message": self.message,
            "is_read": self.is_read,
            "related_application_id": self.related_application_id,
            "related_program_id": self.related_program_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "time_ago": self.get_time_ago(),
        }
    
    def get_time_ago(self) -> str:
        """Return human-readable time ago string"""
        if not self.created_at:
            return "Unknown"
        
        now = datetime.utcnow()
        diff = now - self.created_at
        
        if diff.days > 365:
            years = diff.days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
        elif diff.days > 30:
            months = diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        elif diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
