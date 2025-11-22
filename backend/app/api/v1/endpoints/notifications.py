from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.notification import Notification
from app.dependencies.auth import get_current_active_user
from app.schemas.notification import NotificationResponse, NotificationUpdate

router = APIRouter()


@router.get("/", response_model=List[NotificationResponse])
async def list_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    unread_only: bool = Query(False),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of current user's notifications"""
    query = select(Notification).where(Notification.user_id == current_user.id)
    
    if unread_only:
        query = query.where(Notification.is_read == False)
    
    query = query.offset(skip).limit(limit).order_by(Notification.created_at.desc())
    
    result = await db.execute(query)
    notifications = result.scalars().all()
    
    return notifications


@router.get("/unread-count", response_model=dict)
async def get_unread_count(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get count of unread notifications"""
    result = await db.execute(
        select(Notification).where(and_(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        ))
    )
    count = len(result.scalars().all())
    
    return {"unread_count": count}


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get specific notification by ID"""
    result = await db.execute(
        select(Notification).where(and_(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        ))
    )
    notification = result.scalar_one_or_none()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return notification


@router.patch("/{notification_id}", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: int,
    notification_data: NotificationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Mark notification as read/unread"""
    result = await db.execute(
        select(Notification).where(and_(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        ))
    )
    notification = result.scalar_one_or_none()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = notification_data.is_read
    
    await db.commit()
    await db.refresh(notification)
    
    return notification


@router.post("/mark-all-read", response_model=dict)
async def mark_all_read(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Mark all notifications as read"""
    await db.execute(
        update(Notification)
        .where(and_(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        ))
        .values(is_read=True)
    )
    
    await db.commit()
    
    return {"message": "All notifications marked as read"}


@router.delete("/{notification_id}", status_code=204)
async def delete_notification(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete notification"""
    result = await db.execute(
        select(Notification).where(and_(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        ))
    )
    notification = result.scalar_one_or_none()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    await db.delete(notification)
    await db.commit()
    
    return None
