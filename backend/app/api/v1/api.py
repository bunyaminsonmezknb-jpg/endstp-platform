"""
API Router v1
"""
from fastapi import APIRouter

# =========================================================
# ✅ API ROUTER INSTANCE (EN BAŞTA OLMALI)
# =========================================================
api_router = APIRouter()

# =========================================================
# IMPORTS
# =========================================================

# Core endpoints
from app.api.v1.endpoints import auth, feedback, test_entry, feature_flags
from app.api.v1.endpoints.student import router as student_router
from app.api.v1.endpoints.student_trend import router as student_trend_router

# Motors adapters
from app.motors.priority.adapter import router as priority_router
from app.motors.difficulty.adapter import router as difficulty_router
from app.motors.time_pace.adapter import router as time_pace_router

# Admin router
from app.api.v1.endpoints.admin import router as admin_router

# =========================================================
# ROUTER INCLUDES
# =========================================================

# Auth
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Student
api_router.include_router(student_router, prefix="/student", tags=["student"])
api_router.include_router(student_trend_router)

# Test Entry
api_router.include_router(test_entry.router, tags=["test-entry"])

# Feedback
api_router.include_router(feedback.router, tags=["feedback"])

# Feature Flags
api_router.include_router(feature_flags.router, prefix="/flags", tags=["feature-flags"])

# Motors
api_router.include_router(priority_router)
api_router.include_router(difficulty_router)
api_router.include_router(time_pace_router)

# Admin Panel
api_router.include_router(admin_router.router, prefix="/admin", tags=["admin"])
# =========================================================
# NOTES:
# - Admin router main.py'de ayrı olarak include ediliyor idi şimdi tek bir router altında toplandı
# - Unified motors şimdilik kapalı. 
# =========================================================