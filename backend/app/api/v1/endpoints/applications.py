from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.user import User
from app.models.application import Application, ApplicationStatus
from app.models.program import Program
from app.models.activity import Activity
from app.dependencies.auth import get_current_active_user
from app.schemas.application import (
    ApplicationResponse,
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationWithProgram
)

router = APIRouter()


@router.get("/", response_model=List[ApplicationWithProgram])
async def list_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[ApplicationStatus] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of current user's applications"""
    query = select(Application).options(selectinload(Application.program))
    query = query.where(Application.user_id == current_user.id)
    
    if status:
        query = query.where(Application.status == status)
    
    query = query.offset(skip).limit(limit).order_by(Application.created_at.desc())
    
    result = await db.execute(query)
    applications = result.scalars().all()
    
    # Convert to response format with program data
    response = []
    for app in applications:
        app_dict = app.to_dict()
        app_dict['program'] = app.program.to_dict() if app.program else {}
        response.append(ApplicationWithProgram(**app_dict))
    
    return response


@router.get("/{application_id}", response_model=ApplicationWithProgram)
async def get_application(
    application_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get specific application by ID"""
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.program))
        .where(and_(
            Application.id == application_id,
            Application.user_id == current_user.id
        ))
    )
    application = result.scalar_one_or_none()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    app_dict = application.to_dict()
    app_dict['program'] = application.program.to_dict() if application.program else {}
    
    return ApplicationWithProgram(**app_dict)


@router.post("/", response_model=ApplicationResponse, status_code=201)
async def create_application(
    application_data: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new application"""
    # Verify program exists
    result = await db.execute(
        select(Program).where(Program.id == application_data.program_id)
    )
    program = result.scalar_one_or_none()
    
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    # Generate application ID
    app_count = await db.execute(
        select(Application).where(Application.user_id == current_user.id)
    )
    count = len(app_count.scalars().all())
    
    application_id = f"{program.university[:3].upper()}-{datetime.now().year}-{count + 1:03d}"
    
    # Create application
    application = Application(
        user_id=current_user.id,
        program_id=application_data.program_id,
        application_id=application_id,
        notes=application_data.notes,
        status=ApplicationStatus.DRAFT,
        progress=0
    )
    
    db.add(application)
    
    # Log activity
    activity = Activity(
        user_id=current_user.id,
        action_type="application_created",
        description=f"Started application for {program.program_name} at {program.university}",
        related_entity_type="application",
        related_entity_id=application.id
    )
    db.add(activity)
    
    await db.commit()
    await db.refresh(application)
    
    return application


@router.patch("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: int,
    application_data: ApplicationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update application"""
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.program))
        .where(and_(
            Application.id == application_id,
            Application.user_id == current_user.id
        ))
    )
    application = result.scalar_one_or_none()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Update fields
    update_data = application_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(application, field, value)
    
    # Log activity if status changed
    if 'status' in update_data:
        activity = Activity(
            user_id=current_user.id,
            action_type="application_status_changed",
            description=f"Application status changed to {update_data['status']} for {application.program.program_name}",
            related_entity_type="application",
            related_entity_id=application.id
        )
        db.add(activity)
    
    await db.commit()
    await db.refresh(application)
    
    return application


@router.post("/{application_id}/submit", response_model=ApplicationResponse)
async def submit_application(
    application_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Submit application"""
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.program))
        .where(and_(
            Application.id == application_id,
            Application.user_id == current_user.id
        ))
    )
    application = result.scalar_one_or_none()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if application.status != ApplicationStatus.DRAFT:
        raise HTTPException(status_code=400, detail="Application has already been submitted")
    
    # Update status
    application.status = ApplicationStatus.SUBMITTED
    application.submitted_at = datetime.utcnow()
    application.progress = 100
    
    # Log activity
    activity = Activity(
        user_id=current_user.id,
        action_type="application_submitted",
        description=f"Submitted application for {application.program.program_name} at {application.program.university}",
        related_entity_type="application",
        related_entity_id=application.id
    )
    db.add(activity)
    
    await db.commit()
    await db.refresh(application)
    
    return application


@router.delete("/{application_id}", status_code=204)
async def delete_application(
    application_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete application"""
    result = await db.execute(
        select(Application).where(and_(
            Application.id == application_id,
            Application.user_id == current_user.id
        ))
    )
    application = result.scalar_one_or_none()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    await db.delete(application)
    await db.commit()
    
    return None
