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

# app/api/v1/api.py
from app.motors.priority.adapter import router as priority_router

api_router.include_router(priority_router)

from app.motors.difficulty.adapter import router as difficulty_router
api_router.include_router(difficulty_router)

from app.motors.time_pace.adapter import router as time_pace_router
api_router.include_router(time_pace_router)

# from app.motors.unified.adapter import router as unified_router
# api_router.include_router(unified_router)

# from app.api.v1.endpoints.student.motors.unified import router as unified_motor_router

# api_router.include_router(unified_motor_router)
