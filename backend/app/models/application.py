"""
Application model - User's university applications
"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum as SQLEnum, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class ApplicationStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    REVIEW = "review"
    INTERVIEW = "interview"
    OFFER = "offer"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class Application(Base):
    __tablename__ = "applications"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    program_id = Column(String, ForeignKey("programs.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Application tracking
    application_id = Column(String(50), unique=True, nullable=False, index=True)  # External ID like HAR-2024-001
    status = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.DRAFT, nullable=False, index=True)
    
    # Dates
    submitted_date = Column(DateTime, nullable=True)
    deadline = Column(DateTime, nullable=False)
    decision_date = Column(DateTime, nullable=True)
    
    # Additional info
    action_required = Column(String(500), nullable=True)  # What user needs to do next
    days_left = Column(Integer, nullable=True)  # Computed field for deadline
    notes = Column(Text, nullable=True)
    
    # Progress tracking
    completion_percentage = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="applications")
    program = relationship("Program", back_populates="applications")
    
    def __repr__(self):
        return f"<Application {self.application_id} - {self.status}>"
    
    def to_dict(self, include_relations=False):
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "program_id": self.program_id,
            "application_id": self.application_id,
            "status": self.status.value if self.status else None,
            "submitted_date": self.submitted_date.isoformat() if self.submitted_date else None,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "decision_date": self.decision_date.isoformat() if self.decision_date else None,
            "action_required": self.action_required,
            "days_left": self.days_left,
            "notes": self.notes,
            "completion_percentage": self.completion_percentage,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_relations:
            if self.program:
                data["program"] = self.program.to_dict()
        
        return data
