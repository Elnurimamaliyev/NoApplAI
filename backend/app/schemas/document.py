from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.document import DocumentType, DocumentStatus


class DocumentUpload(BaseModel):
    filename: str
    document_type: DocumentType
    application_id: Optional[int] = None


class DocumentUpdate(BaseModel):
    document_type: Optional[DocumentType] = None
    application_id: Optional[int] = None
    status: Optional[DocumentStatus] = None
    validation_score: Optional[int] = None
    validation_feedback: Optional[str] = None


class DocumentResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    file_path: str
    file_size: int
    document_type: DocumentType
    status: DocumentStatus
    application_id: Optional[int] = None
    validation_score: Optional[int] = None
    validation_feedback: Optional[str] = None
    uploaded_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentWithUrl(DocumentResponse):
    download_url: str

    class Config:
        from_attributes = True
