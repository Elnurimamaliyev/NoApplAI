from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
from datetime import datetime
import os
import uuid

from app.core.database import get_db
from app.models.user import User
from app.models.document import Document, DocumentType, DocumentStatus
from app.models.activity import Activity
from app.dependencies.auth import get_current_active_user
from app.schemas.document import DocumentResponse, DocumentUpdate, DocumentWithUrl

router = APIRouter()


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    document_type: Optional[DocumentType] = None,
    status: Optional[DocumentStatus] = None,
    application_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of current user's documents"""
    query = select(Document).where(Document.user_id == current_user.id)
    
    if document_type:
        query = query.where(Document.document_type == document_type)
    
    if status:
        query = query.where(Document.status == status)
    
    if application_id:
        query = query.where(Document.application_id == application_id)
    
    query = query.offset(skip).limit(limit).order_by(Document.uploaded_at.desc())
    
    result = await db.execute(query)
    documents = result.scalars().all()
    
    return documents


@router.get("/{document_id}", response_model=DocumentWithUrl)
async def get_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get specific document by ID with download URL"""
    result = await db.execute(
        select(Document).where(and_(
            Document.id == document_id,
            Document.user_id == current_user.id
        ))
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # TODO: Generate presigned S3 URL
    download_url = f"/api/v1/documents/{document_id}/download"
    
    doc_dict = document.to_dict()
    doc_dict['download_url'] = download_url
    
    return DocumentWithUrl(**doc_dict)


@router.post("/upload", response_model=DocumentResponse, status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    document_type: DocumentType = Query(...),
    application_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Upload a new document"""
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = f"documents/{current_user.id}/{unique_filename}"
    
    # TODO: Upload to S3/MinIO
    # For now, save file size from content
    content = await file.read()
    file_size = len(content)
    
    # Create document record
    document = Document(
        user_id=current_user.id,
        filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        document_type=document_type,
        status=DocumentStatus.PENDING,
        application_id=application_id
    )
    
    db.add(document)
    
    # Log activity
    activity = Activity(
        user_id=current_user.id,
        action_type="document_uploaded",
        description=f"Uploaded {document_type} document: {file.filename}",
        related_entity_type="document",
        related_entity_id=document.id
    )
    db.add(activity)
    
    await db.commit()
    await db.refresh(document)
    
    return document


@router.patch("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: int,
    document_data: DocumentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update document metadata"""
    result = await db.execute(
        select(Document).where(and_(
            Document.id == document_id,
            Document.user_id == current_user.id
        ))
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Update fields
    update_data = document_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(document, field, value)
    
    await db.commit()
    await db.refresh(document)
    
    return document


@router.delete("/{document_id}", status_code=204)
async def delete_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete document"""
    result = await db.execute(
        select(Document).where(and_(
            Document.id == document_id,
            Document.user_id == current_user.id
        ))
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # TODO: Delete from S3/MinIO
    
    await db.delete(document)
    await db.commit()
    
    return None


@router.get("/{document_id}/download")
async def download_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Download document file"""
    result = await db.execute(
        select(Document).where(and_(
            Document.id == document_id,
            Document.user_id == current_user.id
        ))
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # TODO: Stream from S3/MinIO
    raise HTTPException(status_code=501, detail="Download not yet implemented")


@router.post("/{document_id}/validate", response_model=DocumentResponse)
async def validate_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Trigger AI validation for document"""
    result = await db.execute(
        select(Document).where(and_(
            Document.id == document_id,
            Document.user_id == current_user.id
        ))
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # TODO: Trigger Celery task for AI validation
    document.status = DocumentStatus.VALIDATING
    
    await db.commit()
    await db.refresh(document)
    
    return document
