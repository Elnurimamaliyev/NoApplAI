"""
Models package initialization
"""
from app.models.user import User, UserRole
from app.models.program import Program
from app.models.application import Application, ApplicationStatus
from app.models.document import Document, DocumentType, DocumentStatus
from app.models.notification import Notification, NotificationType
from app.models.activity import Activity, ActivityType

__all__ = [
    "User",
    "UserRole",
    "Program",
    "Application",
    "ApplicationStatus",
    "Document",
    "DocumentType",
    "DocumentStatus",
    "Notification",
    "NotificationType",
    "Activity",
    "ActivityType",
]
