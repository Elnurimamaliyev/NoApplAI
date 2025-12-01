from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProgramBase(BaseModel):
    university_name: str
    program_name: str
    degree_type: str
    country: str
    city: Optional[str] = None
    logo: Optional[str] = None
    color: Optional[str] = None
    application_fee: Optional[str] = None
    deadline: Optional[datetime] = None
    duration_months: Optional[int] = None
    tuition_per_year: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    features: Optional[List[str]] = Field(default_factory=list)
    min_gpa: Optional[float] = None
    english_test_required: Optional[bool] = True
    min_toefl_score: Optional[int] = None
    min_ielts_score: Optional[float] = None
    required_documents: Optional[List[str]] = Field(default_factory=list)
    description: Optional[str] = None
    program_url: Optional[str] = None
    acceptance_rate: Optional[float] = None
    is_active: Optional[bool] = True
    is_featured: Optional[bool] = False


class ProgramCreate(ProgramBase):
    pass


class ProgramUpdate(BaseModel):
    university_name: Optional[str] = None
    program_name: Optional[str] = None
    degree_type: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    logo: Optional[str] = None
    color: Optional[str] = None
    application_fee: Optional[str] = None
    deadline: Optional[datetime] = None
    duration_months: Optional[int] = None
    tuition_per_year: Optional[str] = None
    tags: Optional[List[str]] = None
    features: Optional[List[str]] = None
    min_gpa: Optional[float] = None
    english_test_required: Optional[bool] = None
    min_toefl_score: Optional[int] = None
    min_ielts_score: Optional[float] = None
    required_documents: Optional[List[str]] = None
    description: Optional[str] = None
    program_url: Optional[str] = None
    acceptance_rate: Optional[float] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None


class ProgramResponse(ProgramBase):
    id: str
    created_at: datetime
    updated_at: datetime
    average_match_score: Optional[float] = None

    class Config:
        from_attributes = True


class ProgramRecommendation(BaseModel):
    program: ProgramResponse
    match_score: float
    match_reasons: List[str]

