"""
API Router v1
"""
from app.api.v1.endpoints import feedback
from fastapi import APIRouter
from app.api.v1.endpoints import auth, student, admin_osym, admin_exams, test_entry
from app.api.v1.endpoints import student_todays_tasks

api_router = APIRouter()

# Auth
api_router.include_router(auth.router, tags=["auth"])

# Student
api_router.include_router(student.router, tags=["student"])

# Test Entry (YENİ!)
api_router.include_router(test_entry.router, tags=["test-entry"])

# Admin
api_router.include_router(admin_osym.router, prefix="/admin", tags=["admin-osym"])
api_router.include_router(admin_exams.router, prefix="/admin", tags=["admin-exams"])
api_router.include_router(feedback.router, tags=["feedback"])
api_router.include_router(
    student_todays_tasks.router,
    tags=["student"]
)