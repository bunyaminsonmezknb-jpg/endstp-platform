"""
API Router v1
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, feedback, test_entry
# from app.api.v1.endpoints.student import router as student_router
from app.api.v1.endpoints import feature_flags

api_router = APIRouter()

# Auth
api_router.include_router(auth.router, tags=["auth"])

# Student
# api_router.include_router(student_router, prefix="/student", tags=["student"])

# ✅ TEST ENTRY (SUBJECTS + TOPICS BURADA)
api_router.include_router(test_entry.router, tags=["test-entry"])

# Admin
# api_router.include_router(admin_osym.router, prefix="/admin", tags=["admin-osym"])
# api_router.include_router(admin_exams.router, prefix="/admin", tags=["admin-exams"])

# Feedback
api_router.include_router(feedback.router, tags=["feedback"])

# feature flags
api_router.include_router(feature_flags.router, prefix="/flags", tags=["feature-flags"])