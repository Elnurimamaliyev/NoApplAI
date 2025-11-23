"""
Document model - User uploaded documents
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum, Integer, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class DocumentType(str, enum.Enum):
    CV_RESUME = "CV_RESUME"
    TRANSCRIPT = "TRANSCRIPT"
    ENGLISH_TEST = "ENGLISH_TEST"
    LANGUAGE_CERTIFICATE = "ENGLISH_TEST"  # Alias for backwards compatibility
    RECOMMENDATION_LETTER = "RECOMMENDATION_LETTER"
    STATEMENT_OF_PURPOSE = "STATEMENT_OF_PURPOSE"
    PORTFOLIO = "PORTFOLIO"
    OTHER = "OTHER"


class DocumentStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    VERIFIED = "verified"
    REJECTED = "rejected"
    MISSING = "missing"
    PENDING_VERIFICATION = "pending_verification"


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Document info
    document_type = Column(SQLEnum(DocumentType), nullable=False)
    name = Column(String(255), nullable=False)  # Display name like "CV / Resume"
    filename = Column(String(255), nullable=False)  # Original filename
    file_path = Column(String(500), nullable=False)  # S3 path or URL
    file_size = Column(Integer, nullable=False)  # Size in bytes
    mime_type = Column(String(100), nullable=False)
    
    # Status
    status = Column(SQLEnum(DocumentStatus), default=DocumentStatus.UPLOADED, nullable=False)
    is_verified = Column(Boolean, default=False)
    
    # AI Validation Results
    validation_score = Column(Integer, nullable=True)  # 0-100 quality score
    validation_notes = Column(String(500), nullable=True)
    
    # Optional: Link to specific application
    application_id = Column(String, ForeignKey("applications.id", ondelete="SET NULL"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    verified_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="documents")
    
    def __repr__(self):
        return f"<Document {self.name} - {self.status}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "document_type": self.document_type.value if self.document_type else None,
            "name": self.name,
            "filename": self.filename,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "size_formatted": self.get_size_formatted(),
            "mime_type": self.mime_type,
            "status": self.status.value if self.status else None,
            "is_verified": self.is_verified,
            "validation_score": self.validation_score,
            "validation_notes": self.validation_notes,
            "application_id": self.application_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
        }
    
    def get_size_formatted(self) -> str:
        """Return formatted file size"""
        if not self.file_size:
            return "0 B"
        
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
