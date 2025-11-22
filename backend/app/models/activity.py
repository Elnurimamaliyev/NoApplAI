"""
Activity model - User activity tracking for timeline
"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class ActivityType(str, enum.Enum):
    DOCUMENT_UPLOAD = "document_upload"
    APPLICATION_SUBMIT = "application_submit"
    APPLICATION_UPDATE = "application_update"
    PROFILE_UPDATE = "profile_update"
    AI_MATCH = "ai_match"
    OFFER_RECEIVED = "offer_received"
    DOCUMENT_VERIFIED = "document_verified"


class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Activity info
    activity_type = Column(SQLEnum(ActivityType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Related entities
    related_application_id = Column(String, ForeignKey("applications.id", ondelete="SET NULL"), nullable=True)
    related_document_id = Column(String, ForeignKey("documents.id", ondelete="SET NULL"), nullable=True)
    related_program_id = Column(String, ForeignKey("programs.id", ondelete="SET NULL"), nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="activities")
    
    def __repr__(self):
        return f"<Activity {self.title}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "activity_type": self.activity_type.value if self.activity_type else None,
            "title": self.title,
            "description": self.description,
            "related_application_id": self.related_application_id,
            "related_document_id": self.related_document_id,
            "related_program_id": self.related_program_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "time_ago": self.get_time_ago(),
        }
    
    def get_time_ago(self) -> str:
        """Return human-readable time ago string"""
        if not self.created_at:
            return "Unknown"
        
        now = datetime.utcnow()
        diff = now - self.created_at
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
