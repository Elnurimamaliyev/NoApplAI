"""
Program (University Program) model
"""
from sqlalchemy import Column, String, Integer, Float, Text, JSON, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Program(Base):
    __tablename__ = "programs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    university_name = Column(String(255), nullable=False, index=True)
    program_name = Column(String(255), nullable=False, index=True)
    degree_type = Column(String(50), nullable=False)  # Bachelor, Master, PhD
    
    # Location & Basic Info
    country = Column(String(100), nullable=False, index=True)
    city = Column(String(100), nullable=True)
    logo = Column(String(10), nullable=True)  # Single letter for avatar
    color = Column(String(50), nullable=True)  # Gradient color class
    
    # Application Details
    application_fee = Column(String(20), nullable=True)
    deadline = Column(DateTime, nullable=True)
    duration_months = Column(Integer, nullable=True)
    tuition_per_year = Column(String(50), nullable=True)
    
    # Features & Tags
    tags = Column(JSON, default=list)  # ['Scholarships', 'Fast Decision', etc.]
    features = Column(JSON, default=list)
    
    # Requirements
    min_gpa = Column(Float, nullable=True)
    english_test_required = Column(Boolean, default=True)
    min_toefl_score = Column(Integer, nullable=True)
    min_ielts_score = Column(Float, nullable=True)
    required_documents = Column(JSON, default=list)
    
    # Description
    description = Column(Text, nullable=True)
    program_url = Column(String(500), nullable=True)
    
    # AI Matching (computed fields, can be cached)
    average_match_score = Column(Float, default=0.0)
    acceptance_rate = Column(Float, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    applications = relationship("Application", back_populates="program", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Program {self.university_name} - {self.program_name}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "university_name": self.university_name,
            "program_name": self.program_name,
            "degree_type": self.degree_type,
            "country": self.country,
            "city": self.city,
            "logo": self.logo,
            "color": self.color,
            "application_fee": self.application_fee,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "duration_months": self.duration_months,
            "tuition_per_year": self.tuition_per_year,
            "tags": self.tags,
            "features": self.features,
            "min_gpa": self.min_gpa,
            "english_test_required": self.english_test_required,
            "min_toefl_score": self.min_toefl_score,
            "min_ielts_score": self.min_ielts_score,
            "required_documents": self.required_documents,
            "description": self.description,
            "program_url": self.program_url,
            "average_match_score": self.average_match_score,
            "acceptance_rate": self.acceptance_rate,
            "is_active": self.is_active,
            "is_featured": self.is_featured,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
