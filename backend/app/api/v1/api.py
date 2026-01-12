"""
API Router v1
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, feedback, test_entry
from app.api.v1.endpoints.student import router as student_router  # ✅ AÇILDI
from app.api.v1.endpoints import feature_flags

api_router = APIRouter()

# Auth
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Student (MODULAR - dashboard, tasks, analytics, etc.)
api_router.include_router(student_router, prefix="/student", tags=["student"])  # ✅ AÇILDI

# Test Entry (SUBJECTS + TOPICS BURADA)
api_router.include_router(test_entry.router, tags=["test-entry"])

# Feedback
api_router.include_router(feedback.router, tags=["feedback"])

# Feature flags
api_router.include_router(feature_flags.router, prefix="/flags", tags=["feature-flags"])
