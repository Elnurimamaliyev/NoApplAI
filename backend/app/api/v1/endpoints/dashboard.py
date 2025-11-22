from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from datetime import datetime, timedelta
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.application import Application, ApplicationStatus
from app.models.document import Document
from app.models.notification import Notification
from app.models.activity import Activity
from app.models.program import Program
from app.dependencies.auth import get_current_active_user
from app.schemas.dashboard import (
    DashboardData,
    DashboardStats,
    ActivityItem,
    UpcomingDeadline
)

router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get dashboard statistics for current user"""
    
    # Count applications by status
    app_result = await db.execute(
        select(Application).where(Application.user_id == current_user.id)
    )
    applications = app_result.scalars().all()
    
    total_applications = len(applications)
    active_applications = len([a for a in applications if a.status in [
        ApplicationStatus.DRAFT, ApplicationStatus.SUBMITTED, ApplicationStatus.UNDER_REVIEW
    ]])
    submitted_applications = len([a for a in applications if a.status != ApplicationStatus.DRAFT])
    accepted_applications = len([a for a in applications if a.status == ApplicationStatus.OFFER_RECEIVED])
    
    # Count documents
    doc_result = await db.execute(
        select(func.count(Document.id)).where(Document.user_id == current_user.id)
    )
    documents_uploaded = doc_result.scalar() or 0
    
    # Count upcoming deadlines (within 30 days)
    thirty_days_from_now = datetime.utcnow() + timedelta(days=30)
    deadline_result = await db.execute(
        select(Application)
        .join(Program)
        .where(and_(
            Application.user_id == current_user.id,
            Application.status.in_([ApplicationStatus.DRAFT, ApplicationStatus.SUBMITTED]),
            Program.deadline <= thirty_days_from_now,
            Program.deadline >= datetime.utcnow()
        ))
    )
    upcoming_deadlines = len(deadline_result.scalars().all())
    
    return DashboardStats(
        total_applications=total_applications,
        active_applications=active_applications,
        submitted_applications=submitted_applications,
        accepted_applications=accepted_applications,
        documents_uploaded=documents_uploaded,
        profile_completion=current_user.profile_completion,
        upcoming_deadlines=upcoming_deadlines
    )


@router.get("/activities", response_model=List[ActivityItem])
async def get_recent_activities(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get recent activity feed for current user"""
    result = await db.execute(
        select(Activity)
        .where(Activity.user_id == current_user.id)
        .order_by(Activity.created_at.desc())
        .limit(limit)
    )
    activities = result.scalars().all()
    
    return activities


@router.get("/deadlines", response_model=List[UpcomingDeadline])
async def get_upcoming_deadlines(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get upcoming application deadlines"""
    result = await db.execute(
        select(Application, Program)
        .join(Program)
        .where(and_(
            Application.user_id == current_user.id,
            Application.status.in_([ApplicationStatus.DRAFT, ApplicationStatus.SUBMITTED]),
            Program.deadline >= datetime.utcnow()
        ))
        .order_by(Program.deadline.asc())
        .limit(limit)
    )
    
    deadlines = []
    for application, program in result.all():
        days_left = (program.deadline - datetime.utcnow()).days
        deadlines.append(UpcomingDeadline(
            application_id=application.id,
            program_name=program.program_name,
            university=program.university,
            deadline=program.deadline,
            days_left=days_left,
            status=application.status
        ))
    
    return deadlines


@router.get("/", response_model=DashboardData)
async def get_dashboard_data(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get complete dashboard data"""
    
    # Get stats
    stats_result = await get_dashboard_stats(db=db, current_user=current_user)
    
    # Get activities
    activities_result = await get_recent_activities(limit=5, db=db, current_user=current_user)
    
    # Get deadlines
    deadlines_result = await get_upcoming_deadlines(limit=5, db=db, current_user=current_user)
    
    # Get unread notifications count
    notif_result = await db.execute(
        select(func.count(Notification.id)).where(and_(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        ))
    )
    unread_notifications = notif_result.scalar() or 0
    
    return DashboardData(
        stats=stats_result,
        recent_activities=activities_result,
        upcoming_deadlines=deadlines_result,
        unread_notifications=unread_notifications
    )
