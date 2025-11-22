"""
API v1 Router - combines all endpoint routers
"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    programs,
    applications,
    documents,
    notifications,
    dashboard
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(programs.router, prefix="/programs", tags=["Programs"])
api_router.include_router(applications.router, prefix="/applications", tags=["Applications"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
