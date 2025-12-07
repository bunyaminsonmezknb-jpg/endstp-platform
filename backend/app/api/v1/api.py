"""
API Router v1
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, admin_osym, admin_exams, test_entry, feedback
from app.api.v1.endpoints.student import router as student_router

api_router = APIRouter()

# Auth
api_router.include_router(auth.router, tags=["auth"])

# Student
api_router.include_router(student_router, tags=["student"])

# Test Entry
api_router.include_router(test_entry.router, tags=["test-entry"])

# Admin
api_router.include_router(admin_osym.router, prefix="/admin", tags=["admin-osym"])
api_router.include_router(admin_exams.router, prefix="/admin", tags=["admin-exams"])

# Feedback
api_router.include_router(feedback.router, tags=["feedback"])