from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class DashboardStats(BaseModel):
    total_applications: int
    active_applications: int
    submitted_applications: int
    accepted_applications: int
    documents_uploaded: int
    profile_completion: int
    upcoming_deadlines: int


class ActivityItem(BaseModel):
    id: int
    action_type: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True


class UpcomingDeadline(BaseModel):
    application_id: int
    program_name: str
    university: str
    deadline: datetime
    days_left: int
    status: str


class DashboardData(BaseModel):
    stats: DashboardStats
    recent_activities: List[ActivityItem]
    upcoming_deadlines: List[UpcomingDeadline]
    unread_notifications: int
