from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.application import ApplicationStatus


class ApplicationBase(BaseModel):
    program_id: int
    notes: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None
    submitted_at: Optional[datetime] = None


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    program_id: int
    application_id: str
    status: ApplicationStatus
    progress: int
    notes: Optional[str] = None
    submitted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    # Computed field
    days_left: Optional[int] = None

    class Config:
        from_attributes = True


class ApplicationWithProgram(ApplicationResponse):
    program: dict  # Will contain program details

    class Config:
        from_attributes = True
