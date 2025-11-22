from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProgramBase(BaseModel):
    university: str
    program_name: str
    degree_type: str
    location: str
    deadline: datetime
    description: Optional[str] = None
    requirements: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    features: Optional[List[str]] = Field(default_factory=list)
    min_gpa: Optional[float] = None
    min_sat: Optional[int] = None
    min_act: Optional[int] = None
    min_toefl: Optional[int] = None
    min_ielts: Optional[float] = None


class ProgramCreate(ProgramBase):
    pass


class ProgramUpdate(BaseModel):
    university: Optional[str] = None
    program_name: Optional[str] = None
    degree_type: Optional[str] = None
    location: Optional[str] = None
    deadline: Optional[datetime] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    tags: Optional[List[str]] = None
    features: Optional[List[str]] = None
    min_gpa: Optional[float] = None
    min_sat: Optional[int] = None
    min_act: Optional[int] = None
    min_toefl: Optional[int] = None
    min_ielts: Optional[float] = None


class ProgramResponse(ProgramBase):
    id: int
    created_at: datetime
    updated_at: datetime
    average_match_score: Optional[float] = None

    class Config:
        from_attributes = True


class ProgramRecommendation(BaseModel):
    program: ProgramResponse
    match_score: float
    match_reasons: List[str]
