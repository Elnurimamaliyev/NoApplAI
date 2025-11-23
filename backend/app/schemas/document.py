from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.document import DocumentType, DocumentStatus


class DocumentUpdate(BaseModel):
    document_type: Optional[DocumentType] = None
    application_id: Optional[str] = None
    status: Optional[DocumentStatus] = None
    validation_score: Optional[int] = None
    validation_notes: Optional[str] = None


class DocumentResponse(BaseModel):
    id: str
    user_id: str
    document_type: DocumentType
    name: Optional[str] = None
    filename: str
    file_path: str
    file_size: int
    mime_type: Optional[str] = None
    status: DocumentStatus
    is_verified: Optional[bool] = False
    validation_score: Optional[int] = None
    validation_notes: Optional[str] = None
    application_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    verified_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DocumentWithUrl(DocumentResponse):
    download_url: str

    class Config:
        from_attributes = True
